from django.db import models
from content.models import Category,Tag
from interviewsquestions.utilities.database import languageField
class Poll(models.Model):
    title=models.CharField(max_length=100)
    text=models.TextField()
    categories=models.ManyToManyField(Category,related_name='polls')
    tags=models.ManyToManyField(Tag,related_name='polls')
    language=languageField
    isPublished=models.BooleanField(default=False)
class PollItem(models.Model):
    typeChoices=[ 
        ('R','Radio'),
        ('C','Check'),
    ]
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE)
    type=models.CharField(max_length=1,choices=typeChoices)
    options=models.JSONField()
    class types:
        Radio='R'
        Check='C'