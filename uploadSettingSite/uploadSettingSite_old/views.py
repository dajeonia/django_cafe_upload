from telnetlib import STATUS
from django.http import HttpResponse, JsonResponse
from .main_func import main_function
import os
def test(request):
    main_function()
    return HttpResponse(status=200)

def addCron(request):
    os.system('python manage.py crontab add')
    return HttpResponse(status=200)

def showCron(request):
    os.system('python manage.py crontab show')
    return HttpResponse(status=200)

def removeCron(request):
    os.system('python manage.py crontab remove')
    return HttpResponse(status=200)