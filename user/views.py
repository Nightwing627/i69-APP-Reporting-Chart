from dj_rest_auth.views import LoginView
from django.conf import settings
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.validators import ip_address_validator_map
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from requests import api
from requests.api import request
from rest_framework import fields, status
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.app_settings import (
    JWTSerializer,
    JWTSerializerWithExpiration,
    LoginSerializer,
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    TokenSerializer,
    UserDetailsSerializer,
    create_token,
)
from rest_framework import generics
from django.db.models import Q
from django.shortcuts import get_object_or_404
import uuid
from django.db.models import Count
import django_filters.rest_framework
from rest_framework import filters

from user.models import User, UserPhoto, WorkerInvitation, UserRole
from user import serializers


# Create your views here.


class JWTLoginView(LoginView):
    def get_response_serializer(self):
        if getattr(settings, "REST_USE_JWT", True):
            if getattr(settings, "JWT_AUTH_RETURN_EXPIRATION", True):
                response_serializer = JWTSerializerWithExpiration
            else:
                response_serializer = JWTSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data["user"]

        if getattr(settings, "REST_USE_JWT", True):
            self.access_token, self.refresh_token = jwt_encode(self.user)
        else:
            self.token = create_token(
                self.token_model,
                self.user,
                self.serializer,
            )

        if getattr(settings, "REST_SESSION_LOGIN", True):
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, "REST_USE_JWT", True):
            from rest_framework_simplejwt.settings import (
                api_settings as jwt_settings,
            )

            access_token_expiration = (
                timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
            )
            refresh_token_expiration = (
                timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
            )
            return_expiration_times = getattr(
                settings, "JWT_AUTH_RETURN_EXPIRATION", True
            )

            data = {
                "user": self.user,
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
            }

            if return_expiration_times:
                data["access_token_expiration"] = access_token_expiration
                data["refresh_token_expiration"] = refresh_token_expiration

            serializer = serializer_class(
                instance=data,
                context=self.get_serializer_context(),
            )
        else:
            serializer = serializer_class(
                instance=self.token,
                context=self.get_serializer_context(),
            )

        response = Response(serializer.data, status=status.HTTP_200_OK)
        if getattr(settings, "REST_USE_JWT", True):
            from dj_rest_auth.jwt_auth import set_jwt_cookies

            set_jwt_cookies(response, self.access_token, self.refresh_token)
        return response

    pass


class UserListView(
    generics.ListCreateAPIView,
):
    queryset = (
        User.objects.all()
        .annotate(roles_count=Count("roles"))
        .filter(Q(roles_count=0) and ~Q(email__endswith="i69app.com"))
        .filter(is_staff=False)
        .filter(is_superuser=False)
    )

    serializer_class = serializers.UserSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = []
    search_fields = ["fullName"]


user_list_view = UserListView.as_view()


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = "id"


user_detail_view = UserDetailView.as_view()


class WorkerListView(
    generics.ListAPIView,
):
    queryset = (
        User.objects.all()
        .filter(Q(roles__role__in=["ADMIN", "SUPER_ADMIN", "CHATTER"]))
        .distinct("id")
    )
    serializer_class = serializers.UserSerializer


worker_list_view = WorkerListView.as_view()


class GenerateWorkerInvitationView(APIView):
    def get(self, request, key=""):
        print(key)
        try:
            invitation = WorkerInvitation.objects.filter(token=key)
        except ValidationError:
            return Response({"messsage": f"{key} is not a valid UUID"}, status=400)
        if len(invitation) == 0:
            return Response({"message": "invalid invitation key"}, status=401)
        invitation = invitation[0]
        return Response({"email": invitation.email, "key": key})

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({}, status=401)
        roles = [r.role for r in request.user.roles.all()]
        if "ADMIN" not in roles and "SUPER_ADMIN" not in roles:
            return Response({}, status=401)
        data = request.data
        data.pop("generated", None)
        data.pop("link_value", None)
        token = uuid.uuid4()
        email = request.data.get("email", None)
        is_admin_permission = request.data.get("is_admin_permission", None)
        is_chat_admin_permission = request.data.get("is_chat_admin_permission", None)
        if (
            email != None
            and is_admin_permission != None
            and is_chat_admin_permission != None
        ):
            invitation = WorkerInvitation(token=token, **data)
            invitation.save()
            return Response({"link": f"/#/signUp/?invitationKey={token}"})
        else:
            return Response(
                {
                    "message": "email, is_admin_permission and is_chat_admin_permission required"
                },
                status=400,
            )


generate_worker_invitation_view = GenerateWorkerInvitationView.as_view()


def authorize_is_worker_or_owner(request, id):
    # authorization
    if str(request.user.id) != id and len(request.user.roles.all()) == 0:
        return Response(
            {"reason": "You are not authorized to upload photo for this user"},
            status=401,
        )


class PhotoUploadView(APIView):
    def delete(self, request, id):
        res = authorize_is_worker_or_owner(request, id)
        if res:
            return res
        photo_id = request.body.get("id")
        photo = get_object_or_404(UserPhoto, id=photo_id)
        if photo.user.id != request.user.id:
            return Response({}, status=401)
        photo.delete()
        return Response({})

    def post(self, request, id):
        try:
            res = authorize_is_worker_or_owner(request, id)
            if res:
                return res

            user = get_object_or_404(User, id=id)
            # check count of already uploaded photos
            if user.avatar_photos.count() >= user.photos_quota:
                return Response(
                    {"reason": "You can only upload 4 photos for free"}, status=401
                )

            url = ""
            photo = request.data.get("photo", None)
            img_url = request.data.get("url", None)
            if not photo and not img_url:
                return Response({"reason": "photo or url form-data required"}, status=400)

            if photo:
                up = UserPhoto(file=photo, user=user)
                up.save()
                url = request.build_absolute_uri(up.file.url)
            else:
                url = img_url
                up = UserPhoto(url=url, user=user)
                up.save()

            return Response({"url": url, "id": up.id})
        except Exception as e:
            return Response({"reason": f"unkown exception: {e}"}, status=500)


photo_upload_view = PhotoUploadView.as_view()


class WorkerSignupView(APIView):
    def post(self, request):
        try:
            serializer = serializers.SignUpRequestSerialzier(request.data)
            data = serializer.data
            key = data.pop("invitation_key")
            invitation = WorkerInvitation.objects.filter(token=key)
        except ValidationError as e:
            return Response(e, status=400)

        if len(invitation) == 0:
            return Response({"message": "invalid invitaion key"}, status=400)
        invitation = invitation[0]
        data["email"] = invitation.email
        data["username"] = data["first_name"] + data["last_name"]
        data.pop("first_name")
        data.pop("last_name")
        password = data.pop("password")
        try:
            user = User(**data)
            user.set_password(password)
            user.save()

            if invitation.is_admin_permission:
                user.roles.get(UserRole.ROLE_ADMIN)
            if invitation.is_chat_admin_permission:
                user.roles.add(UserRole.ROLE_CHATTER)
                user.roles.add(UserRole.ROLE_REGULAR)
            user.save()

            return Response(serializers.UserSerializer(user).data, status=201)
        except Exception as e:
            print(e)
            return Response({"message": "undefined error occured"}, status=500)


worker_signup_view = WorkerSignupView.as_view()


class UserLikeView(APIView):
    def post(self, request, id, friend_id):
        if not request.user.is_authenticated:
            return Response(
                {"non_field_errors": ["unauthenticated request not allowed"]},
                status=401,
            )
        roles = {r.role for r in request.user.roles.all()}
        if len(roles) == 0 and not request.user.is_superuser:
            return Response({}, status=401)
        user1 = get_object_or_404(User, id=id)
        user2 = get_object_or_404(User, id=friend_id)
        if user2 in user1.likes.all():
            return Response({"message": "like connection already exists"}, status=200)
        user1.likes.add(user2)
        user2.likes.add(user1)
        user1.save()
        user2.save()
        return Response({"message": "created like connection"}, status=201)


user_like_view = UserLikeView.as_view()


class DeleteReportsView(APIView):
    def delete(self, request, id):
        if not request.user.is_authenticated:
            return Response(
                {"non_field_errors": ["unauthenticated request not allowed"]},
                status=401,
            )
        roles = {r.role for r in request.user.roles.all()}
        if len(roles) == 0 and not request.user.is_superuser:
            return Response({}, status=401)
        user = get_object_or_404(User, id=id)
        user.reports.all().delete()
        return Response({}, status=200)


delete_reports_view = DeleteReportsView.as_view()
