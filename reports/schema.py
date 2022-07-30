from django.urls import reverse

from reports.models import Reported_Users
from reports.models import GoogleAuth
import graphene
from user.models import *
from django.db.models import F
from framework.api.API_Exception import APIException
import requests
from django.contrib.auth import get_user_model

from requests_oauthlib import OAuth1
from urllib.parse import urlencode

from social.apps.django_app.default.models import UserSocialAuth

from dj_rest_auth.serializers import TokenSerializer
from dj_rest_auth.utils import default_create_token
from rest_framework.authtoken.models import Token


def get_token(user):
    if not user:
        return ""
    token = default_create_token(Token, user, TokenSerializer)
    return token.key


class reportResponseObj(graphene.ObjectType):
    id = graphene.String()


class reportUser(graphene.Mutation):
    class Arguments:
        timestamp = graphene.DateTime()
        reporter = graphene.String()
        reportee = graphene.String()

    Output = reportResponseObj

    def mutate(self, info, timestamp, reporter, reportee):
        report = Reported_Users.objects.create(
            timestamp=timestamp,
            reporter=reporter,
            reportee=reportee,
        )
        user = get_user_model().objects.get(id=reporter)
        blckd_user = get_user_model().objects.get(id=reportee)
        user.blockedUsers.add(blckd_user)
        report.save()
        print(Reported_Users.id)
        return reportResponseObj(id=report.id)


class googleAuthResponse(graphene.ObjectType):
    email = graphene.String()
    is_new = graphene.Boolean()
    id = graphene.String()
    token = graphene.String()
    username = graphene.String()


class twitterAuthResponse(graphene.ObjectType):
    twitter = graphene.String()
    username = graphene.String()
    is_new = graphene.Boolean()
    id = graphene.String()
    token = graphene.String()

def check_is_new(user: User):
    """
        Check whether a user is not properly initialized
    """
    if user.age == None or user.fullName == '' or user.height == None or user.avatar_photos.all().count() == 0:
        return True
    return False

class SocialAuth(graphene.Mutation):
    class Arguments:
        access_token = graphene.String(required=True)
        provider = graphene.String(required=True)
        access_verifier = graphene.String(default_value="")

    Output = googleAuthResponse

    def mutate(self, info, access_token, provider, access_verifier=""):
        try:
            if "google" in provider.lower():
                idinfo = requests.get(
                    f"https://oauth2.googleapis.com/tokeninfo?id_token={access_token}"
                )
                idinfo = idinfo.json()
                if idinfo.get("error") == "invalid_token":
                    return Exception("Invalid Token")
            if "facebook" in provider.lower():
                redirect_url = "https://api.i69app.com"
                # idinfo = requests.get(
                #     f"https://graph.facebook.com/oauth/access_token?client_id=1610603699070152&client_secret=cc752b4e78233fe6df148dc6305fb6d0&grant_type=client_credentials&redirect_uri={redirect_url}")
                idinfo = requests.get(
                    f"https://graph.facebook.com/me?fields=name,email&access_token={access_token}"
                )
                idinfo = idinfo.json()
                if idinfo.get("error") == "invalid_token":
                    return Exception("Invalid Token")
            if "twitter" in provider.lower():
                oauth = OAuth1(
                    settings.SOCIAL_AUTH_TWITTER_KEY,
                    client_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                    resource_owner_key=access_token,
                    verifier=access_verifier,
                )
                res = requests.post(
                    f"https://api.twitter.com/oauth/access_token", auth=oauth
                )

                res_split = res.text.split("&")
                if len(res_split) >= 4:
                    oauth_token = res_split[0].split("=")[1]
                    oauth_secret = res_split[1].split("=")[1]
                    user_id = res_split[2].split("=")[1] if len(res_split) > 2 else None
                    user_name = (
                        res_split[3].split("=")[1]+"_twitter" if len(res_split) > 3 else None
                    )
                else:
                    return Exception(res.text)

                if user_id == None or user_name == None:
                    return Exception("Invalied token")
                else:
                    try:
                        user = get_user_model().objects.get(twitter=user_id)
                        is_new = check_is_new(user)
                    except:
                        user, _ = get_user_model().objects.get_or_create(
                            twitter=user_id,
                            defaults={
                                "password": "",
                                "fullName": user_name,
                                "email": user_id,
                                "username": user_name + "_twitter",
                            },
                        )
                        user.save()
                        is_new = True
                        socialAuth, _ = UserSocialAuth.objects.get_or_create(
                            user_id=user.id,
                            defaults={
                                "provider": provider.lower(),
                                "uid": user_id,
                                "user_id": user.id,
                                "extra_data": "",
                            },
                        )
                        socialAuth.save()

                    return twitterAuthResponse(
                        twitter=user_id,
                        is_new=is_new,
                        id=user.id,
                        token=get_token(user),
                        username=user.username,
                    )

            userCnt = get_user_model().objects.filter(email=idinfo["email"]).count()
            if userCnt > 0:
                user = get_user_model().objects.get(email=idinfo["email"])
                is_new = check_is_new(user)
            else:
                user, _ = get_user_model().objects.get_or_create(
                    email=idinfo["email"],
                    defaults={
                        "password": "",
                        "fullName": idinfo["name"],
                        "email": idinfo["email"],
                        "username": idinfo["email"].replace("@", '_'),
                    },
                )
                user.save()

                socialAuth, _ = UserSocialAuth.objects.get_or_create(
                    user_id=user.id,
                    defaults={
                        "provider": provider.lower(),
                        "uid": idinfo["email"],
                        "user_id": user.id,
                        "extra_data": "",
                    },
                )
                socialAuth.save()

                is_new = True
                g = GoogleAuth.objects.create(
                    email=idinfo["email"], sub=idinfo.get("sub")
                )
                g.save()

            return googleAuthResponse(
                email=idinfo["email"],
                is_new=is_new,
                id=user.id,
                token=get_token(user),
                username=idinfo["email"].replace("@", '_'),
            )
        except ValueError:
            Exception("Invalid Token")



class Mutation(graphene.ObjectType):
    social_auth = SocialAuth.Field()
    reportUser = reportUser.Field()


# class googleAuth(graphene.ObjectType):
