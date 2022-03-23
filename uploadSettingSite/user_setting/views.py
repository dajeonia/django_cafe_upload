from django.http import HttpResponse
from .models import UserSetting
import os
import time

def index(request):
    time.sleep(3)
    os.system('python manage.py crontab remove')
    time.sleep(3)
    os.system('python manage.py crontab add')
    time.sleep(3)
    return HttpResponse({"success":True})
