import graphene
from .models import *
from .tokenbuilder import generate_agora_token


class generateAgoraToken(graphene.ObjectType):
    id = graphene.String()
    token = graphene.String()
    appID = graphene.String()

    def resolve_id(self, info):
        return self['id']

    def resolve_token(self, info):
        return self['token']

    def resolve_appID(self, info):
        return self['appID']


class Query(graphene.ObjectType):
    generateAgoraToken = graphene.Field(generateAgoraToken, id=graphene.String(required=True),
                                        ChannelName=graphene.String(required=True))

    def resolve_generateAgoraToken(self, info, **kwargs):
        id = kwargs.get('id')
        ChannelName = kwargs.get('ChannelName')
        token, appID = generate_agora_token(id, ChannelName)

        tokenlog = AgoraTokenLog.objects.values().first()
        return tokenlog


class SendNotification(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        icon = graphene.String(required=True)
        user_id = graphene.UUID(required=True)
        app_url =graphene.String()
        priority = graphene.Int()
        data = graphene.JSONString()
        android_channel_id = graphene.String()


    sent = graphene.Boolean()

    def mutate(root, info, title, body, icon, user_id, app_url, priority, data, android_channel_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise Exception('User with this ID does not exist.')

        send_notification(title=title, body=body, icon=icon, user=user, app_url=app_url, priority=priority, data=data, android_channel_id=android_channel_id)
        return SendNotification(sent=True)


class Mutation(graphene.ObjectType):
    sendNotification = SendNotification.Field()
