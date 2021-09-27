from django.db import models
from django.db.models.fields import CharField, TextField
from interviewsquestions.settings import MEDIA_ROOT


class AdvertisePage(models.Model):
    langChoices = [
        ('AR','عربي'),
        ('EN','English')
    ]
    title=CharField(max_length=30 ,default='Advertic With Us')        
    language = models.CharField(max_length = 2,choices = langChoices)
    text=models.TextField(default='')

class AdvertiseImage(models.Model):
    page=models.ForeignKey(AdvertisePage,on_delete=models.CASCADE,related_name='images')
    imageFile=models.ImageField(upload_to=MEDIA_ROOT.joinpath('advertise'))

class Service(models.Model):
    langChoices = [
        ('AR','عربي'),
        ('EN','English')
    ]
    title=CharField(max_length=50)
    text=TextField()
    image=models.ImageField(upload_to=MEDIA_ROOT.joinpath('services'))

    language = models.CharField(max_length = 2,choices = langChoices)



class AdvertistRequest(models.Model):
    langChoices = [
    ('AR','عربي'),
    ('EN','English')
    ]


    company=models.CharField(max_length=90)
    email=models.EmailField()
    subject=models.CharField(max_length=200)
    text=models.TextField()
    
    language = models.CharField(max_length = 2,choices = langChoices)


    def __str__(self):
        return self.subject


class NewsUser(models.Model):
    langChoices = [
    ('AR','عربي'),
    ('EN','English')
    ]
    name=models.CharField(max_length=40)
    email=models.EmailField(unique=True)
    language = models.CharField(max_length = 2,choices = langChoices)

class InfoItem(models.Model):
    langChoices = [
    ('AR','عربي'),
    ('EN','English')
    ]
    title=models.CharField(max_length=200)
    text=models.TextField()
    language = models.CharField(max_length = 2,choices = langChoices)


# class SocialMedia(models.Model):
#     nameEN =models.CharField(max_length=40)
#     nameAR =models.CharField(max_length=40)
#     url =models.URLField()
#     icon=models.ImageField(upload_to= MEDIA_ROOT.joinpath('social'))

#     def __str__(self) -> str:
#         return self.name


class ContactMessage(models.Model):
    langChoices = [
    ('AR','عربي'),
    ('EN','English')
    ]
    userName=models.CharField(max_length=50)
    email=models.EmailField()
    subject=models.CharField(max_length=130)
    text=models.TextField()
    language = models.CharField(max_length = 2,choices = langChoices,default='EN')
