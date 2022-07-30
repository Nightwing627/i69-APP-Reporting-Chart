import graphene
from gallery.models import *
from django.db.models import F
# from framework.api.APIException import APIException
from user.models import User


class UserBasicObj(graphene.ObjectType):
    username = graphene.String()
    fullName = graphene.String()

    def resolve_fullName(self, info):
        return self['fullName']

    def resolve_username(self, info):
        return self['username']


class PhotoObj(graphene.ObjectType):
    id = graphene.Int()
    image_data = graphene.String()
    date = graphene.Date()

    def resolve_id(self, info):
        return self['id']

    def resolve_image_data(self, info):
        return self['image_data']

    def resolve_date(self, info):
        return self['date']


class AlbumObj(graphene.ObjectType):
    title = graphene.String()
    date = graphene.Date()
    description = graphene.String()
    # photos = graphene.List(PhotoObj)

    def resolve_title(self, info):
        return self['title']

    def resolve_uploader(self, info):
        return User.objects.values().get(id=self['uploader_id'])

    def resolve_date(self, info):
        return self['date']

    def resolve_description(self, info):
        return self['description']

    @graphene.resolve_only_args
    def resolve_photos(self):
        return Album.objects.values().annotate(
            caption=F('photos__caption'),
            image=F('photos__image_data'),
            date=F('photos__date'),
            uploader=F('photos__uploader')
        ).filter(id=self['id'])

