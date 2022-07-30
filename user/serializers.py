from chatapp import models
from django.db.models import query
from rest_framework.exceptions import server_error
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from user.models import User, UserPhoto
from defaultPicker import models as pickerModels
from reports.serializers import ReportSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["firstName"] = user.first_name
        token["lastName"] = user.last_name
        token["privileges"] = {r.role: True for r in user.roles.all()}
        return token


class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = UserPhoto


class SlugRelatedGetOrCreateField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            return queryset.get_or_create(**{self.slug_field: data})[0]
        except (TypeError, ValueError):
            self.fail("invalid")


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source="fullName")
    reports = ReportSerializer(many=True, read_only=True)
    sign_up = serializers.DateTimeField(source="created_at", read_only=True)
    owner_id = serializers.CharField(max_length=36, write_only=True, required=False)
    # fake_users = RecursiveField(many=True)
    fake_users = serializers.SerializerMethodField()
    roles = serializers.SlugRelatedField(slug_field="role", many=True, read_only=True)
    # owned_by = serializers.SerializerMethodField()
    avatar_photos = UserPhotoSerializer(many=True, read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=pickerModels.tags.objects.all()
    )

    books = SlugRelatedGetOrCreateField(
        slug_field="interest",
        many=True,
        source="book",
        queryset=pickerModels.book.objects.all(),
    )
    sportsTeams = SlugRelatedGetOrCreateField(
        slug_field="interest",
        many=True,
        queryset=pickerModels.sportsTeams.objects.all(),
    )
    tvShows = SlugRelatedGetOrCreateField(
        slug_field="interest", many=True, queryset=pickerModels.tvShows.objects.all()
    )
    music = SlugRelatedGetOrCreateField(
        slug_field="interest", many=True, queryset=pickerModels.music.objects.all()
    )
    movies = SlugRelatedGetOrCreateField(
        slug_field="interest", many=True, queryset=pickerModels.movies.objects.all()
    )

    age = serializers.PrimaryKeyRelatedField(
        queryset=pickerModels.age.objects.all(), required=False, allow_null=True
    )
    height = serializers.PrimaryKeyRelatedField(
        queryset=pickerModels.height.objects.all(), required=False, allow_null=True
    )
    ethnicity = serializers.IntegerField(allow_null=True, source="ethinicity") 
    # ethinicity = serializers.PrimaryKeyRelatedField(queryset=pickerModels.ethnicity.objects.all(), required=False, allow_null=True)
    # zodiacSign = serializers.PrimaryKeyRelatedField(queryset=pickerModels.zodiacSign.objects.all(), required=False, allow_null=True)
    # familyPlans = serializers.PrimaryKeyRelatedField(queryset=pickerModels.family.objects.all(), required=False, allow_null=True)
    # politics = serializers.PrimaryKeyRelatedField(queryset=pickerModels.politics.objects.all(), required=False, allow_null=True)
    # religion = serializers.PrimaryKeyRelatedField(queryset=pickerModels.religious.objects.all(), required=False, allow_null=True)

    def get_owned_by(self, obj):
        data = obj.owned_by.all()
        if len(data) > 0:
            return UserSerializer(data, many=True).data
        return []

    def get_fake_users(self, obj):
        data = obj.fake_users.all()
        if len(data) > 0:
            return UserSerializer(data, many=True).data
        return []

    class Meta:
        model = User
        fields = [
            "books",
            "avatar_photos",
            # "owned_by",
            "is_fake",
            "sign_up",
            "created_at",
            "reports",
            "display_name",
            "id",
            "email",
            "twitter",
            "first_name",
            "last_name",
            "fullName",
            "gender",
            "about",
            "location",
            "isOnline",
            "familyPlans",
            "tags",
            "politics",
            "coins",
            "zodiacSign",
            "interestedIn",
            "interested_in",
            "ethnicity",
            "religion",
            "blockedUsers",
            "education",
            "music",
            "height",
            "age",
            "tvShows",
            "sportsTeams",
            # "sportsTeam",
            "movies",
            "work",
            "is_blocked",
            "username",
            "owner_id",
            "fake_users",
            "roles",
        ]
        extra_kwargs = {
            "owner_id": {"write_only": True},
        }
        read_only_fields = [
            "fake_users",
            # "owned_by"
        ]
        depth = 1

    def create(self, validated_data):
        owner_id = validated_data.pop("owner_id", "")
        user = User.objects.create(**validated_data)
        worker = User.objects.filter(id=owner_id)
        if worker.count():
            worker = worker[0]
            user.owned_by.add(worker)
            user.save()
        return user

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        # Add any custom update logic here
        fields = [
            "books",
            "music",
        ]
        instance.save()
        return instance


class SignUpRequestSerialzier(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    invitation_key = serializers.UUIDField()
    password = serializers.CharField()
