from django.db import models



class EmailTemplate(models.Model):
    langChoices = [
    ('AR','عربي'),
    ('EN','English')
    ]
    name=models.CharField(max_length=60)
    html=models.TextField()
    language = models.CharField(max_length = 2,choices = langChoices)

