from django.db import models
from django.contrib.auth.models import User
from interviewsquestions.utilities.database import languageField
from content.models import Category, Post
from django.utils import timezone
class SuggestedCategory(models.Model):
    name =models.CharField(max_length=60)
    suggester=models.ForeignKey(User,on_delete=models.CASCADE)
    parent=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    language=languageField
    description=models.TextField()
    time=models.DateTimeField(auto_now_add=True)

    def getFormatedDate(self):
        return timezone.localdate(self.time).strftime('%Y/%m/%d')

class SuggestedTag(models.Model):
    suggester=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=60)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField()

class FlagReason(models.Model):
    typeChoices=[ 
        ('Q','Questions'),
        ('A','Answers'),
        ('U','Users'),
    ]
    type=models.CharField(max_length=1,choices=typeChoices)
    nameEN=models.CharField(max_length=50)
    nameAR=models.CharField(max_length=50)
    descEN=models.CharField(max_length=300)
    descAR=models.CharField(max_length=300)
    class types:
        Questions='Q'
        Answers='A'
        Users='U'

class Reports(models.Model):
    reporter=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reportsM')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='reports',null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reports',null=True)
    reason=models.ForeignKey(FlagReason,on_delete=models.CASCADE)
