from django.db import models
from django.core.cache import cache

from interviewsquestions.settings import BASE_DIR


class EmailTemplate(models.Model):
    langChoices = [
    ('AR','عربي'),
    ('EN','English')
    ]
    name=models.CharField(max_length=60)
    html=models.TextField()
    language = models.CharField(max_length = 2,choices = langChoices)


class BoolOption(models.Model):
    key=models.CharField(max_length=25)
    value=models.BooleanField(default=False)

    # Const
    ARABIC_KEY='Arabic'
    def __str__(self):
        return self.key
    @staticmethod
    def arabicOn():
        try:
            if not cache.get('arabic-on') is None:
                return cache.get('arabic-on')
            else:
                value=BoolOption.objects.get(key=BoolOption.ARABIC_KEY).value
                cache.set('arabic-on',value,timeout=None)
                return value 
        except BoolOption.DoesNotExist:
            BoolOption.objects.create(key=BoolOption.ARABIC_KEY)
            cache.set('arabic-on',False)
            return False

    @staticmethod
    def setArabic(value:bool):
        import json
        obj = BoolOption.objects.get(key=BoolOption.ARABIC_KEY)
        obj.value=value            
        obj.save()
        cache.set('arabic-on',value,timeout=None)
        settingsFile=open(str(BASE_DIR/'settings.json'),'r+')
        settingsJSON=json.loads(settingsFile.read())
        settingsJSON[BoolOption.ARABIC_KEY]=value
        settingsFile.seek(0)
        settingsFile.truncate(0)
        settingsFile.write(json.dumps(settingsJSON))
        settingsFile.close()
        return value 
    @staticmethod
    def setValue(key:str,value:bool):
        obj = BoolOption.objects.get(key=key)
        obj.value=value
        obj.save()
        return value 

