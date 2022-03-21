from django.db import models

# Create your models here.
class UserSetting(models.Model):
    """
    id : no
    naver_id : 네이버 아이디
    naver_pw : 네이버 비밀번호
    naver_cid : 개발자센터 cid
    naver_csec : 개발자센터 csecret
    
    is_active : 활성화 여부
    """
    id = models.AutoField(primary_key=True)
    naver_id = models.CharField(max_length=30)
    naver_pw = models.CharField(max_length=30)
    naver_cid = models.CharField(max_length=30)
    naver_csec = models.CharField(max_length=30)

    class Meta:
        db_table = 'user_setting'