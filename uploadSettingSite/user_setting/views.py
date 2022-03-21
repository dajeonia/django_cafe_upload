from django.http import HttpResponse
from .models import UserSetting
import os
import time

def index(request):
    os.system('python manage.py crontab remove')
    time.sleep(5)
    os.system('python manage.py crontab add')
    time.sleep(5)
    return HttpResponse({"success":True})
