from dashboard.models import BoolOption
from django.utils.translation import activate,get_language
from django.conf import settings
from django.utils.translation import LANGUAGE_SESSION_KEY
class  langMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response


    def __call__(self, request):
        response=self.get_response(request)
        if get_language()[:2]=='ar' and not BoolOption.arabicOn():
            activate('en')
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME,'en')
            request.session[LANGUAGE_SESSION_KEY]='en'
        return response