import json
from django.db import models
from content.models import Category,Tag
from interviewsquestions.utilities.database import languageField
from django.contrib.auth.models import User
from django.utils.translation import gettext
class Poll(models.Model):
    title=models.CharField(max_length=100)
    text=models.TextField()
    categories=models.ManyToManyField(Category,related_name='polls')
    tags=models.ManyToManyField(Tag,related_name='polls')
    language=languageField
    isPublished=models.BooleanField(default=False)
    isOpened=models.BooleanField(default=False)
    def userTargeted(self):
        countP=0
        for cate in self.categories.all():
            countP+=cate.users.all().count()
            for sub in cate.getAllSubCategories():
                countP+=sub.users.all().count()
        tagsUser=set()
        for tag in self.tags.all():
            tagsUser=tagsUser.union(set(tag.users.all()))
        tagsUser=set(tagsUser)
        countP+=len(tagsUser)
        return countP
    def rate(self):
        
        return ('%.2f' % ((self.resaults.count()*100)/self.userTargeted()))+'%'
class PollItem(models.Model):
    typeChoices=[ 
        ('R',gettext('Radio List')),
        ('C',gettext('Check List')),
    ]
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE,related_name='items')
    type=models.CharField(max_length=1,choices=typeChoices)
    text=models.TextField()
    options=models.JSONField()
    class types:
        Radio='R'
        Check='C'

    def getOptions(self):
        return json.loads(self.options)
    def getResault(self):
        data={}
        allResaults=self.poll.resaults.all()
        for opt in self.getOptions():
            data[opt]=0
        for resObj in allResaults:
            resault=resObj.resault[str(self.id)]
            for opt in self.getOptions():
                if opt in resault:
                    data[opt]+=1
        finalData=[]
        for d in data.items():
            finalData.append({'name':d[0],'percent':'%.2f'%((d[1]*100)/allResaults.count())})
        return finalData
class PollResault(models.Model):
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE,related_name='resaults')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='pollResaults')
    resault=models.JSONField()
    
    class Meta:
        unique_together=[['poll','user']]