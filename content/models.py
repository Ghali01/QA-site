
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls.base import clear_script_prefix
from interviewsquestions.utilities.database import languageField
# from authusers.models import UserProfile
from django.contrib.auth.models import User
import datetime
import json
class Category(models.Model):
    name =models.CharField(max_length=60)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    language=languageField

    
    def toArray(self):
        subCategories=Category.objects.filter(parent=self)
        data=[]
        for sub in subCategories:
            data.append({
                'name':sub.name,
                'id':sub.id,
                'toArray':sub.toArray(),
                'sub':sub.toArray(),
            }
        )
        return data

    
    def subs(self):
        return json.dumps(self.toArray())
    def subCategoies(self):
         return list(Category.objects.filter(parent=self))
    def getLvl(self):
        target=self
        lvl=1
        while True:
            if target.parent:
                lvl+=1
                target=target.parent
            else:
                return lvl
    def getFirstParent(self):
        lvl =self.getLvl()
        if lvl>1:
            if lvl==2:
                return self.parent
            if lvl==3:
                return self.parent.parent
            if lvl==4:
                return self.parent.parent.parent
        else:
            return None
    def getSecondParent(self):
        lvl =self.getLvl()
        if lvl>2:
            if lvl==3:
                return self.parent
            if lvl==4:
                return self.parent.parent
        else:
            return None
    def getThirdParent(self):
        lvl =self.getLvl()
        if lvl>3:
            return self.parent
        else:
            return None
class Tag(models.Model):
    name=models.CharField(max_length=60)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='tags')
    description=models.TextField()



class Post(models.Model):
    typeChoices=[
        ('Q','Question'),
        ('A','Answer'),
    ]
    text=models.TextField()
    author=models.ForeignKey(User,on_delete=CASCADE)
    votes=models.IntegerField(default=0)
    type=models.CharField(max_length=1,choices=typeChoices)
    isPublished=models.BooleanField(default=False)

    class types:
        Question='Q'
        Answer='A'
class Question(models.Model):
    post=models.OneToOneField(Post,on_delete=models.CASCADE,related_name='question')
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='questions')
    tags=models.ManyToManyField(Tag,related_name='questions')
class SuggestedQuestion(models.Model):
    post=models.OneToOneField(Post,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    tags=models.ManyToManyField(Tag)
    date=models.DateField(auto_now_add=True,)
    
    class Meta:
        ordering=['date']

    def getDuration(self):
        now=datetime.datetime.now().date()
        days =(now - self.date).days
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
    def formatedDate(self):
        return self.date.strftime('%Y/%m/%d')

    def modeWhoAccept(self):
        return self.post.logs.filter(type=PostLog.types.Accept).first().moderator
    def modeWhoReject(self):
        return self.post.logs.filter(type=PostLog.types.Reject).first().moderator

    def isAccepted(self):
        return self.post.logs.filter(type=PostLog.types.Accept).exists()

    def isRejected(self):
        return self.post.logs.filter(type=PostLog.types.Reject).exists()

class PostLog(models.Model):
    typeChoices=[
        ('S','Suggest'),
        ('A','Accept'),
        ('R','Reject'),
        ('E','Edit'),
        ('AE','Accept Edit'),
        ('P','Publish'),
        ('UP','Unpublish'),
    ]
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='logs')
    text=models.TextField(null=True)
    title=models.CharField(max_length=200,null=True)
    moderator=models.ForeignKey(User,on_delete=CASCADE,related_name='logs', null=True)
    author=models.ForeignKey(User,on_delete=CASCADE)
    time=models.TimeField(auto_now_add=True)
    type=models.CharField(max_length=4,choices=typeChoices)
    question=models.OneToOneField(Question,on_delete=models.CASCADE,null=True)
    class Meta:
        ordering=['time']
    class types:
        Suggest='S'
        Accept='A'
        Reject='R'
        Edit='E'
        AcceptEdit='AE'
        Publish='P'
        Unpublish='UP'
