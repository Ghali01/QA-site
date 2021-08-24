from django.urls import path
from main import views
urlpatterns=[
    path('',views.registerPage,name='index'),
    path('register',views.registerPage,name='register-page'),
    path('confirm/<str:code>',views.confirmUser,name='confirm-user'),
    path('email-sent',views.emailSent,name='email-sent'),
    path('login',views.loginPage,name='login-page'),
]