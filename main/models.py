from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.contrib.auth.models import User

class TempUser(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    code=models.CharField(max_length=100,unique=True)
    website=models.CharField(max_length=70)
