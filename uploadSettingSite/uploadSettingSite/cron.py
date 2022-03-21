from datetime import datetime
from user_setting.models import UserSetting
def printTime():
    for user in UserSetting.objects.all():
        print(user.naver_id)
    return