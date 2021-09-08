from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class LoginByEmail(BaseBackend):

    def authenticate(self, request,email,password):
        try:
            user= User.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        return User.objects.get(pk=user_id)