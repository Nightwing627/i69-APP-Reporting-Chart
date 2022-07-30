import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import connection
from rest_framework.authtoken.models import Token
from defaultPicker.models import interestedIn as InterestedIn, tags as Tags, book as Book, music as Music, \
    movies as Movies, sportsTeams as SportsTeams, tvShows as TvShows, height as Height, age as Age

import uuid
from .utils import FAMILY_CHOICE, AGE_RANGE, ETHINICITY_TYPE, POLITICS_CHOICE, RELIGIOUS_CHOICE

from social.apps.django_app.default.models import UserSocialAuth
from django.utils.html import format_html
from django.core.validators import MaxValueValidator, MinValueValidator

class UserRole(models.Model):
    ROLE_REGULAR = 'REGULAR'
    ROLE_CHATTER = 'CHATTER'
    ROLE_ADMIN = 'ADMIN'
    ROLE_SUPER_ADMIN = 'SUPER_ADMIN'

    ROLES = (
        (ROLE_REGULAR, ROLE_REGULAR),
        (ROLE_CHATTER, ROLE_CHATTER),
        (ROLE_ADMIN, ROLE_ADMIN),
        (ROLE_SUPER_ADMIN, ROLE_SUPER_ADMIN),
    )
    role = models.CharField(choices=ROLES, max_length=20, default='REGULAR', null=False)

    def __str__(self):
        return self.role



class User(AbstractUser):
    def get_avatar_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/images/avatar/' + filename

    INTEREST_CHOICES = (
        (1, "SERIOUS_RELATIONSHIP_ONLY_MALE"),
        (2, "SERIOUS_RELATIONSHIP_ONLY_FEMALE"),
        (3, "SERIOUS_RELATIONSHIP_BOTH"),

        (4, "CAUSAL_DATING_ONLY_MALE"),
        (5, "CAUSAL_DATING_ONLY_FEMALE"),
        (6, "CAUSAL_DATING_BOTH"),

        (7, "NEW_FRIENDS_ONLY_MALE"),
        (8, "NEW_FRIENDS_ONLY_FEMALE"),
        (9, "NEW_FRIENDS_BOTH"),

        (10, "ROOM_MATES_ONLY_MALE"),
        (11, "ROOM_MATES_ONLY_FEMALE"),
        (12, "ROOM_MATES_BOTH"),

        (13, "BUSINESS_CONTACTS_ONLY_MALE"),
        (14, "BUSINESS_CONTACTS_ONLY_FEMALE"),
        (15, "BUSINESS_CONTACTS_BOTH")
    )
    GENDER_CHOICES = (
        (0, 'Male'),
        (1, 'Female'),
        (2, 'Prefer not to say'),
    )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, null=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    twitter = models.CharField(
        max_length=255, default='', blank=True, verbose_name='Twitter')
    first_name = None
    last_name = None
    fullName = models.CharField(
        max_length=255, default='', blank=True, verbose_name='Full Name')
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES, blank=True, null=True)
    about = models.CharField(max_length=255, default='',
                             blank=True, verbose_name='Bio')
    location = models.CharField(max_length=255, default='', blank=True)
    isOnline = models.BooleanField(default=False)
    familyPlans = models.PositiveBigIntegerField(
        choices=FAMILY_CHOICE, null=True, blank=True)
    # age = models.PositiveBigIntegerField(choices=AGE_RANGE, blank=True, null=True)
    tags = models.ManyToManyField(
        Tags, related_name='profile_tags', blank=True)
    politics = models.PositiveBigIntegerField(
        choices=POLITICS_CHOICE, blank=True, null=True)
    coins = models.PositiveIntegerField(null=False, default=0)
    zodiacSign = models.PositiveBigIntegerField(blank=True, null=True)
    # height = models.IntegerField(null=True, blank=True, default=0)
    # interestedIn = models.PositiveSmallIntegerField(choices=INTEREST_CHOICES, null=True, blank=True)
    interestedIn = models.CharField(max_length=256, blank=True, null=True)
    interested_in = models.CharField(max_length=256, blank=True, null=True)
    ethinicity = models.PositiveBigIntegerField(
        choices=ETHINICITY_TYPE, blank=True, null=True)
    religion = models.PositiveBigIntegerField(
        choices=RELIGIOUS_CHOICE, blank=True, null=True)
        
    # list of users this user has blocked, they can't message him now
    blockedUsers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='blocked_by')
    
    # set this to true to block a user from using the app
    is_blocked = models.BooleanField(default=False)

    education = models.CharField(max_length=265, null=True, blank=True)

    music = models.ManyToManyField(Music, blank=True)
    height = models.ForeignKey(
        Height, blank=True, null=True, verbose_name='Height', on_delete=models.CASCADE)
    age = models.ForeignKey(Age, blank=True, null=True,
                            verbose_name='Age', on_delete=models.CASCADE)
    tvShows = models.ManyToManyField(TvShows, blank=True)
    sportsTeams = models.ManyToManyField(SportsTeams, blank=True)
    movies = models.ManyToManyField(Movies, blank=True)
    work = models.CharField(max_length=265, null=True, blank=True)
    book = models.ManyToManyField(Book, blank=True)
    likes = models.ManyToManyField('self', blank=True,related_name='author')
    photos_quota = models.SmallIntegerField(default=3)
    avatar = models.TextField(null=True, blank=True)
    # avatar = models.ImageField()
    owned_by = models.ManyToManyField('User', null=True, blank=True, related_name='fake_users')

    onesignal_player_id = models.CharField(max_length=256, blank=True, null=True)
    roles = models.ManyToManyField('UserRole', related_name='users', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    @property
    def is_fake(self):
        return 'i69app.com' in self.email
    
    @property
    def interestedIn_display(self):
        return list(map(int, self.interested_in.split(','))) if self.interested_in else []
    def image_tag(self):
        from django.utils.html import escape
        return u'<img src="%s" />'
    def socialProvider(self):
        cursor = connection.cursor()
        cursor.execute("SELECT provider FROM social_auth_usersocialauth where user_id=%s", [str(self.id).replace('-', '')])
        row = cursor.fetchone()
        if row == None:
            return ''
        else:
            return format_html('<img style="width: 25px;height: 25px;" src="/static/admin/img/{}.png">', row[0].split('-')[0])

    socialProvider.short_description = 'Provider'
    socialProvider.allow_tags = True
    avatar.short_description = 'Image'
    avatar.allow_tags = True


def content_file_name(instance, filename):
    name, ext = filename.split('.')
    file_path = 'photos/user_{user_id}/{name}.{ext}'.format(
          user_id=instance.user.id,
          name=uuid.uuid4(), 
          ext=ext,
        ) 
    return file_path

class UserPhoto(models.Model):
    file = models.ImageField(upload_to=content_file_name, null=True, blank=True)
    file_url = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avatar_photos', null=True)

    def __str__(self):
        return f"{self.user} {self.pk}"


class UserSocialProfile(models.Model):
    SOCIAL_PROFILE_PLATFORMS = (
        (1, 'GOOGLE'),
        (2, 'FACEBOOK'),
        (3, 'INSTAGRAM'),
        (4, 'SNAPCHAT'),
        (5, 'LINKEDIN'),
        (6, 'REDDIT')
    )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.PositiveSmallIntegerField(
        choices=SOCIAL_PROFILE_PLATFORMS, default=4)
    url = models.URLField()

    class Meta:
        verbose_name_plural = "User Social Profiles"
        verbose_name = "User Social Profile"

    def __str__(self):
        return str(self.user.username) + ' - ' + str(self.platform)


class CoinSettings(models.Model):
    method = models.CharField(max_length=70)
    coins_needed = models.IntegerField()

    def __str__(self):
        return self.method + " --- " + str(self.coins_needed)


class WorkerInvitation(models.Model):
    email = models.EmailField()
    token = models.UUIDField()
    is_admin_permission = models.BooleanField()
    is_chat_admin_permission = models.BooleanField()

    def __str__(self):
        return self.email