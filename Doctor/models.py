from django.db import models


# Create your models here.


class Doctor(models.Model):
    dusername = models.CharField(max_length=100, unique=True)
    dpassword = models.CharField(max_length=100)

    class Meta:
        db_table = 'doctor_doctors'

    def __str__(self):
        return u'UserInfo:{}'.format(self.dusername)
