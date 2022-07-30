from datetime import date
from django.db import models
from django.contrib.auth import get_user_model
from user.models import User
from django.utils.safestring import mark_safe
class Photo(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    image_data = models.TextField(null=True, blank=True)
    def image_tag(self):
        if self.image_data:
            if 'data:image/' in self.image_data:
                return mark_safe('<img src="%s" style="width: 100px; height:100px;" />' % self.image_data)
            else:
                return mark_safe('<img src="data:image/png;base64,%s" style="width: 100px; height:100px;" />' % self.image_data)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'
    # def __str__(self):
    #     return str(self.image_tag)
    class Meta:
        verbose_name_plural = "Photos"
        verbose_name = "Photo"


class Album(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(default=date.today)
    description = models.TextField(null=True, blank=True)
    photos = models.ManyToManyField(Photo, related_name='album')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Albums"
        verbose_name = "Album"
