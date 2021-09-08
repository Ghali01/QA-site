from django.db import models
from interviewsquestions.utilities.database import languageField
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
                'sub':sub.toArray()
            }
        )
        return data
    def subs(self):
        return json.dumps(self.toArray())

class Tag(models.Model):
    name=models.CharField(max_length=60)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='tags')
    description=models.TextField()
