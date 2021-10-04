from django.db import models
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils import timezone
from interviewsquestions.settings import MEDIA_ROOT
from content.models import Post, Badge, PostLog, Tag,Question
import datetime
from interviewsquestions.utilities.database import langChoices
from feedback.models import FlagReason
from django.utils.translation import get_language
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
    website=models.CharField(max_length=70,null=True,default='')
    about=models.TextField(null=True,default='')
    image=models.ImageField(upload_to='profile/',default='profile/default.jpg')
    tags=models.ManyToManyField(Tag)
    permission=models.CharField(max_length=3,choices=permissionsChoies,default='U')
    socialID=models.CharField(max_length=150,unique=True,null=True)
    provider=models.CharField(max_length=20,choices=providerChoises,null=True)
    favQuestions=models.ManyToManyField(Question)
    followers=models.ManyToManyField(User)
    rep=models.IntegerField(default=0)
    badges=models.ManyToManyField(Badge,through='BadgesUser')
    views=models.PositiveBigIntegerField(default=0)
    lastActive=models.DateTimeField(auto_now_add=True)
    language=models.CharField(max_length=2,choices=langChoices,default='en')
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
    def goldBadges(self):
        return self.badges.filter(level=Badge.levels.Gold)
    def silverBadges(self):
        return self.badges.filter(level=Badge.levels.Silver)
    def bronzeBadges(self):
        return self.badges.filter(level=Badge.levels.Bronze)
    def answersCount(self):
        return Post.objects.filter(type=Post.types.Answer,author=self.user,logs__type=PostLog.types.Accept).count()
    def questionsCount(self):
        return Question.objects.filter(post__author=self.user).count()
    def joinData(self):
        now=datetime.datetime.now().date()
        days =(now - self.user.date_joined.date()).days
        if days ==0:
            return 'today'
        elif days == 1:
            return 'yesterday'
        elif days<30:
            return str(days) +' days'
        elif days >= 30 and days<356:
            return str(int(days/30))+' months'
        elif days >= 365:
            if days % 365 < 30:
                return str(int(days/365))+' years'
            elif days % 365 >=30 :
                return str(int(days/365))+' years '+ str(int(days%365/30)) + ' months'
    def lastSeen(self):
        now=timezone.now()
        seconds=(now - self.lastActive).seconds
        if seconds<60:
            return str(seconds)+' secs'
        elif seconds <3600:
            return str(int(seconds/60)) + ' min'
        elif seconds <86400:
            return str(int(seconds/3600)) + ' hour'
        days =(now - self.user.date_joined.date()).days
        if days ==0:
            return 'today'
        elif days == 1:
            return 'yesterday'
        elif days<30:
            return str(days) +' days'
        elif days >= 30 and days<356:
            return str(int(days/30))+' months'
        elif days >= 365:
            if days % 365 < 30:
                return str(int(days/365))+' years'
            elif days % 365 >=30 :
                return str(int(days/365))+' years '+ str(int(days%365/30)) + ' months'
    def getViews(self):
        if self.views < 1000:
            return self.views
        elif self.views < 1000000:
            return int(self.views/1000)+'K'
        else:
            return int(self.views/1000000)+'M'
    def lastTwoGold(self):
        return BadgesUser.objects.filter(badge__level=Badge.levels.Gold,profile=self)[:2]
    def lastTwoSilver(self):
        return BadgesUser.objects.filter(badge__level=Badge.levels.Silver,profile=self)[:2]
    def lastTwoBronze(self):
        return BadgesUser.objects.filter(badge__level=Badge.levels.Bronze,profile=self)[:2]
    def updateLastSeen(self):
        self.lastActive=timezone.now()
        self.save()
    def isOnline(self):
        now=timezone.now()
        seconds=(now - self.lastActive).seconds
        if seconds<= 300:
            return True
        else:
            return False
    def getReports(self):
        lang=get_language()[:2]
        reasons=FlagReason.objects.filter(type=FlagReason.types.Users)
        data=[]
        for reason in reasons:
            count=self.user.reports.filter(reason=reason).count()
            name=reason.nameEN if lang=='en' else reason.nameAR
            if count>0:
                data.append({
                    'name':name,
                    'count':count,
                    'id':reason.id
                })

        return data
class BadgesUser(models.Model):
    profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    badge=models.ForeignKey(Badge,on_delete=models.CASCADE) 
    date=models.DateField(auto_now_add=True)
    class Meta:
        ordering=['-date']
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