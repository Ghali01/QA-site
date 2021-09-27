from django.db import models
from django.contrib.auth.models import User
from interviewsquestions.settings import MEDIA_ROOT
from content.models import Badge, Tag,Question

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
    image=models.ImageField(upload_to='profile/',default='profile/default.jpg')
    tags=models.ManyToManyField(Tag)
    permission=models.CharField(max_length=3,choices=permissionsChoies,default='U')
    socialID=models.CharField(max_length=150,unique=True,null=True)
    provider=models.CharField(max_length=20,choices=providerChoises,null=True)
    favQuestions=models.ManyToManyField(Question)
    followers=models.ManyToManyField(User)
    rep=models.IntegerField()
    badges=models.ManyToManyField(Badge)
    def isBaned(self):
        return BanedUser.objects.filter(user=self.user).exists()
    def isModerator(self):
        return self.permission=='M'
    def isSuperAdmin(self):
        return self.permission=='SA'
    def isAdmin(self):
        return self.permission=='A'
    def goldBadgesCount(self):
        return self.badges.filter(level=Badge.levels.Gold).count()
    def silverBadgesCount(self):
        return self.badges.filter(level=Badge.levels.Silver).count()
    def bronzeBadgesCount(self):
        return self.badges.filter(level=Badge.levels.Bronze).count()
class SocialUser(models.Model):
    fullName=models.CharField(max_length=100,null=True)
    email=models.EmailField()
    image=models.URLField()
    socialID=models.CharField(max_length=150,unique=True)
    provider=models.CharField(max_length=20,choices=providerChoises)
    
    
    class Meta():
        unique_together=['provider','socialID']


class BanedUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)