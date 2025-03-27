from django.db import models

class Students(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    course = models.CharField(max_length=50)
    batch = models.IntegerField()
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'students'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_full_name = models.CharField(max_length=255, blank=True, null=True)
    user_email = models.CharField(max_length=255, blank=True, null=True)
    user_password = models.CharField(max_length=255, blank=True, null=True)
    user_phone = models.CharField(max_length=20)
    user_phonenumber = models.IntegerField()
    phone_number = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Users(models.Model):
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'users'

