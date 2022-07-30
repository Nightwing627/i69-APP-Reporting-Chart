from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
import json

from django.db import models

from django.conf import settings
import uuid
from django.db.models import constraints

from onesignal_sdk.client import Client

User = get_user_model()


class AgoraTokenLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    token = models.CharField(max_length=265, null=False)
    appID = models.CharField(max_length=265, null=False)
    creator = models.CharField(max_length=265, null=False)

    def __str__(self):
        return self.token + " - " + " - " + self.creator


def send_notification(title, body, icon, user, app_url=None, data=None, priority=None, android_channel_id=None):
    notification_body = {
        "headings": {"en": title},
        "contents": {"en": body},
        "small_icon": icon,
        "include_player_ids": [user.onesignal_player_id],
        # 'filters': [{'field': 'tag', 'key': 'level', 'relation': '>', 'value': 10}],
    }
    if app_url:
        notification_body["app_url"] = app_url
    if data:
        notification_body["data"] = data
    if priority:
        notification_body["priority"] = priority
    if android_channel_id:
        notification_body["android_channel_id"] = android_channel_id
    client = Client(
        app_id=settings.ONESIGNAL_APP_ID, rest_api_key=settings.ONESIGNAL_REST_API_KEY
    )
    try:
        response = client.send_notification(notification_body)
        if response.body.get("errorZs"):
            raise Exception(response.body["errors"][0])
        return response
    except Exception as e:
        if hasattr(e, "message"):
            raise Exception(e.message)
        raise e
