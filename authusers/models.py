from django.db import models
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from content.models import Tag
from interviewsquestions.settings import MEDIA_ROOT
class TempUser(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='tmp')
    code=models.CharField(max_length=100,unique=True)
    website=models.CharField(max_length=70)


providerChoises=[
    ('fa','Facebook'),
    ('tw','Twitter'),
    ('go','Google'),
    ('gi','Github'),
]

class UserProfile(models.Model):
    permissionsChoies=[
        ('SA','Super Admin'),
        ('A','Admin'),
        ('M','Moderator'),
        ('U','User')
        ]
    
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    website=models.CharField(max_length=70,null=True)
    about=models.TextField(null=True)
    image=models.ImageField(upload_to=MEDIA_ROOT.joinpath('profile'),default='profile/default.jpg')
    tags=models.ManyToManyField(Tag)
    permission=models.CharField(max_length=3,choices=permissionsChoies,default='U')
    socialID=models.CharField(max_length=150,unique=True,null=True)
    provider=models.CharField(max_length=20,choices=providerChoises,null=True)


class SocialUser(models.Model):
    fullName=models.CharField(max_length=100,null=True)
    email=models.EmailField()
    image=models.URLField()
    socialID=models.CharField(max_length=150,unique=True)
    provider=models.CharField(max_length=20,choices=providerChoises)
    
    
    class Meta():
        unique_together=['provider','socialID']