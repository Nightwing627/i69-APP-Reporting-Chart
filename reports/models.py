from django.db import models
import datetime

from django.utils.timezone import now

# Create your models here.

class Reported_Users(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    timestamp = models.DateTimeField(default=now)
    # Reporter and Reportee can be null for backwards compatibility 
    reporter = models.ForeignKey('user.User', related_name="reported_list", on_delete=models.DO_NOTHING, null=True)
    reportee = models.ForeignKey('user.User', related_name='reports', on_delete=models.DO_NOTHING, null=True)
    reason = models.CharField(max_length=255)


    class Meta:
        verbose_name_plural = "Reported Users"
        verbose_name = "Reported Users"
    
    def __str__(self):
        return str(self.reporter) + ' - ' + str(self.reportee) + ' ---- ' + str(self.timestamp)

class GoogleAuth(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    email = models.EmailField(null=True, blank=True)
    sub = models.CharField(max_length=200, null=True, blank=True)
