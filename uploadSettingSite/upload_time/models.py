from django.db import models

# Create your models here.
class UploadTime(models.Model):
    """
    id : no
    upload_hr : 업로드 시간(시)
    upload_mn : 업로드 시간(분)
    """
    id = models.AutoField(primary_key=True)
    upload_hr = models.IntegerField()
    upload_mn = models.IntegerField()

    class Meta:
        db_table = 'upload_time'