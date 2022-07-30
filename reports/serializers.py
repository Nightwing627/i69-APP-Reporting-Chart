from django.db import models
from django.db.models.query import QuerySet
from rest_framework import serializers
from reports.models import Reported_Users
from user.models import User

class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    reportee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Reported_Users
        fields = ['reporter', 'reportee', 'reason']