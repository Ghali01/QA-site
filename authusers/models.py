from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

from content.models import Post, Badge, PostLog, Tag,Question,Category
import datetime
from interviewsquestions.utilities.database import langChoices
from feedback.models import FlagReason
from django.utils.translation import get_language,gettext,pgettext
class TempUser(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='tmp')
    code=models.CharField(max_length=100,unique=True)
    website=models.CharField(max_length=70)


providerChoises=[
    ('fa',gettext('Facebook')),
    ('tw',gettext('Twitter')),
    ('go',gettext('Google')),
    ('gi',gettext('Github')),
]


class UserProfile(models.Model):
    permissionsChoies=[
        ('SA',gettext('Super Admin')),
        ('A',gettext('Admin')),
        ('M',gettext('Moderator')),
        ('U',gettext('User'))
        ]
    
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    website=models.CharField(max_length=70,null=True,default='')
    about=models.TextField(null=True,default='')
    image=models.ImageField(upload_to='profile/',default='profile/default.jpg')
    tags=models.ManyToManyField(Tag,related_name='users')
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
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='users')
    loginTimes=models.PositiveIntegerField(default=0)
    def polls(self):
        polls=[]
        for res in self.user.userResaults.all():
            polls.append(res.poll)

        return polls
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
            return gettext('today')
        elif days == 1:
            return gettext('yesterday')
        elif days<30:
            return str(days) +' '+gettext('days')
        elif days >= 30 and days<356:
            return str(int(days/30))+' '+gettext('months')
        elif days >= 365:
            if days % 365 < 30:
                return str(int(days/365))+' '+gettext('years')
            elif days % 365 >=30 :
                return str(int(days/365))+' '+gettext('years')+' '+ str(int(days%365/30)) + ' '+gettext('months')
    def lastSeen(self):
        now=timezone.now()
        seconds=(now - self.lastActive).seconds
        if seconds<60:
            return str(seconds)+' '+gettext('secs')
        elif seconds <3600:
            return str(int(seconds/60)) + ' '+gettext('min')
        elif seconds <86400:
            return str(int(seconds/3600)) + ' '+gettext('hour')
        days =(now - self.user.date_joined.date()).days
        if days ==0:
            return gettext('today')
        elif days == 1:
            return gettext('yesterday')
        elif days<30:
            return str(days) +' '+gettext('days')
        elif days >= 30 and days<356:
            return str(int(days/30))+' '+gettext('months')
        elif days >= 365:
            if days % 365 < 30:
                return str(int(days/365))+' '+gettext('years')
            elif days % 365 >=30 :
                return str(int(days/365))+' '+gettext('years')+' '+ str(int(days%365/30)) + ' '+gettext('months')
    def getViews(self):
        if self.views < 1000:
            return self.views
        elif self.views < 1000000:
            return int(self.views/1000)+pgettext('count','K')
        else:
            return int(self.views/1000000)+pgettext('count','M')
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


class TmpLink(models.Model):
    # actionChoices=[ 
    #     ('P','Reset Password'),
    #     ('E','Reset Email'),
    # ]
    # action=models.CharField(max_length=1,choices=actionChoices)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    key=models.CharField(max_length=100)
    # class actions:
    #     ResetPassword="P"
    #     ResetEmail="E"