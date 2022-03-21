from inspect import trace
import traceback
import subprocess
import time
from pathlib import Path
from django.shortcuts import render
from user_setting.models import UserSetting
from board_matching.models import BoardMatching
from upload_time.models import UploadTime

BASE_DIR=Path(__file__).resolve().parent.parent

def index(request):
    userList = UserSetting.objects.all()
    uploadTimeList = UploadTime.objects.all()
    selectedUserInfo =None
    uploadList = None
    if 'choose_user' in request.POST:
        try:
            if request.POST['chosen_id']:
                selectedUserInfo = userList.get(id=request.POST['chosen_id'])
                uploadList =BoardMatching.objects.filter(user_no = request.POST['chosen_id'])
        except (KeyError):
            traceback.print_exc()
            print('비정상적인 접근 (KeyError)')
            
        return render(request, 'home/home.html', 
        {
            'user_list':userList,
            'selected_user_info':selectedUserInfo,
            'upload_list':uploadList,
            'upload_time_list':uploadTimeList
        })
    elif 'update_user' in request.POST:
        update_user =  UserSetting.objects.get(id=request.POST['id'])
        update_user.naver_id = request.POST['naver_id']
        update_user.naver_pw = request.POST['naver_pw']
        update_user.naver_cid = request.POST['naver_cid']
        update_user.naver_csec = request.POST['naver_csec']
        update_user.save()
        return render(request, 'home/home.html', 
        {
            'user_list':userList,
            'upload_time_list':uploadTimeList
        })
    elif 'create_user' in request.POST:
        user = UserSetting(naver_id=request.POST['naver_id'], naver_pw=request.POST['naver_pw'],
        naver_cid = request.POST['naver_cid'], naver_csec = request.POST['naver_csec'])
        user.save()
        return render(request, 'home/home.html', 
        {
            'user_list':userList,
            'upload_time_list':uploadTimeList
        })
    elif 'delete_user' in request.POST:
        chosen_user = UserSetting.objects.get(id=request.POST['chosen_id'])
        chosen_user.delete()
        return render(request, 'home/home.html', 
        {
            'user_list':userList,
            'upload_time_list':uploadTimeList
        })
    elif 'create_upload_list' in request.POST:
        upload_info = BoardMatching(from_board_url=request.POST['from_board_url'],
        from_club_id=request.POST['from_club_id'],
        from_menu_id=request.POST['from_menu_id'],
        to_board_url=request.POST['to_board_url'],
        to_club_id=request.POST['to_club_id'],
        to_menu_id=request.POST['to_menu_id'],
        from_article_no=request.POST['from_article_no'],
        to_article_no=request.POST['to_article_no'],
        user_no=request.POST['user_id'],
        is_active=True)
        upload_info.save()
        try:
            if request.POST['user_id']:
                selectedUserInfo = userList.get(id=request.POST['user_id'])
                uploadList =BoardMatching.objects.filter(user_no = request.POST['user_id'])



        except (KeyError):
            traceback.print_exc()
            print('비정상적인 접근 (KeyError)')
        return render(request, 'home/home.html', 
        {
            'user_list':userList,
            'selected_user_info':selectedUserInfo,
            'upload_list':uploadList,
            'upload_time_list':uploadTimeList
        })
    elif 'delete_upload_item' in request.POST:
        chosen_upload_item = BoardMatching.objects.get(id = request.POST['upload_item_id'])
        chosen_upload_item.delete()
        try:
            if request.POST['user_id']:
                selectedUserInfo = userList.get(id=request.POST['user_id'])
                uploadList =BoardMatching.objects.filter(user_no = request.POST['user_id'])

        except (KeyError):
            traceback.print_exc()
            print('비정상적인 접근 (KeyError)')

        return render(request, 'home/home.html', 
        {
            'user_list':userList,
            'selected_user_info':selectedUserInfo,
            'upload_list':uploadList,
            'upload_time_list':uploadTimeList
        })
    elif 'create_upload_time' in request.POST:
        UploadTime(upload_hr=int(request.POST['upload_time_hr']), upload_mn=int(request.POST['upload_time_mn'])).save()
        f=open(str(BASE_DIR)+"/uploadSettingSite/cron_setting_info.py", 'w')
        f.write('CRON_INFO = \"'+' '.join([str(upload_time.upload_hr)+":"+str(upload_time.upload_mn) for upload_time in uploadTimeList])+'\"')
        f.close()
        
        result = subprocess.check_output('python manage.py crontab add', shell=True)
        print(result)

        return render(request, 'home/home.html', 
        {
            'user_list':userList,
            'upload_time_list':uploadTimeList
        })
    elif 'delete_upload_time' in request.POST:
        chosen_upload_time = UploadTime.objects.get(id=request.POST['chosen_id'])
        chosen_upload_time.delete()
        f=open(str(BASE_DIR)+"/uploadSettingSite/cron_setting_info.py", 'w')
        f.write('CRON_INFO = \"'+' '.join([str(upload_time.upload_hr)+":"+str(upload_time.upload_mn) for upload_time in uploadTimeList])+'\"')
        f.close()

        result = subprocess.check_output('python manage.py crontab add', shell=True)
        print(result)

        return render(request, 'home/home.html', 
        {
            'user_list':userList,
            'upload_time_list':uploadTimeList
        })
    else:
        return render(request, 'home/home.html',
        {
            'user_list':userList,
            'upload_time_list':uploadTimeList
        })