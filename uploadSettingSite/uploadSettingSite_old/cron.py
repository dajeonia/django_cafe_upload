import datetime
from user_setting.models import UserSetting
def printTime():
    print("\n\n",datetime.datetime.now())
    for user in UserSetting.objects.all():
        print(user.naver_id)
    return