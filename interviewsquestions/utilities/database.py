
from django.db.models import CharField
langChoices=[
    ('ar','عربي'),
    ('en','English')
]

languageField=CharField(max_length=2,choices=langChoices)