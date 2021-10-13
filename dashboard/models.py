from django.db import models



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
            return BoolOption.objects.get(key=BoolOption.ARABIC_KEY).value
        except BoolOption.DoesNotExist:
            BoolOption.objects.create(key=BoolOption.ARABIC_KEY)
            return False

    @staticmethod
    def setArabic(value:bool):
        obj = BoolOption.objects.get(key=BoolOption.ARABIC_KEY)
        obj.value=value
        obj.save()
        return value 
    @staticmethod
    def setValue(key:str,value:bool):
        obj = BoolOption.objects.get(key=key)
        obj.value=value
        obj.save()
        return value 

