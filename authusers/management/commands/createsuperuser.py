from django.core.management.base import BaseCommand,CommandParser
from django.contrib.auth.models import User
from authusers.models import UserProfile
from django.db.utils import IntegrityError
from getpass import getpass
class Command(BaseCommand):

    # def add_arguments(self, parser: CommandParser):
    #     parser.add_argument('fullname',type=str)
    #     parser.add_argument('username',type=str)
    #     parser.add_argument('email',type=str)
    #     parser.add_argument('password',type=str)
    def handle(self, *args, **options):
        fullname=input('enter full name: ')
        username=input('enter user name: ')
        email=input('enter email: ')
        password=getpass('enter password: ')
        confPassword=getpass('enter confirm password: ')
        if not password ==confPassword:
            self.stderr.write('password does not match')
            return
        if len(password)<8:
            self.stderr.write('password should be 8 letters at least')
            return
    
        if User.objects.filter(email=email).exists():
            self.stderr.write('email already exists')
            return
        try:
            user=User.objects.create_superuser(username,email,password,first_name=fullname)
            profile=UserProfile.objects.create(user=user,permission='SA')
            self.stdout.write(self.style.SUCCESS('user created'))
        except IntegrityError:
            self.stderr.write('username already exists')
            