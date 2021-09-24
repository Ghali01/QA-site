from django.db import models
from django.contrib.auth.models import User
from interviewsquestions.utilities.database import languageField
from content.models import Category
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

