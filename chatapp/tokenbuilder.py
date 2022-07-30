import time

from .src.RtcTokenBuilder import RtcTokenBuilder, Role_Attendee
from .models import AgoraTokenLog
from user.models import User

def generate_agora_token(id, channelName):
    user = User.objects.get(id=id)
    appID = 'AGORA_APP_ID'
    appCertificate = 'AGORA_APP_CERTIFICATE'
    channelName = channelName
    userAccount = user.username
    expireTimeInSeconds = 3600
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expireTimeInSeconds

    token = RtcTokenBuilder.buildTokenWithAccount(
        appID, appCertificate, channelName, userAccount, Role_Attendee, privilegeExpiredTs)

    log = AgoraTokenLog(token = token, appID = appID, creator = userAccount)
    log.save()
    print(token)
    print('done token')

    return (token , appID)