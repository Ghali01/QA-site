from django.urls import path
from authusers import views
app_name='authusers'
urlpatterns=[

    path('auth-index',views.index,name='auth-index'),
    path('register',views.registerPage,name='register-page'),
    path('confirm/<str:code>',views.confirmUser,name='confirm-user'),
    path('email-sent',views.emailSent,name='email-sent'),
    path('login',views.loginPage,name='login-page'),
    path('select-tags',views.selectTags,name='select-tags'),
    path('set-email',views.chnageEmail,name='set-email'),
    path('logout',views.logout,name='logout'),
    path('facebook-login',views.facebookLogin,name='facebok-login'),
    path('google-login',views.googelLogin,name='google-login'),
    path('github-login',views.githubLogin,name='github-login'),
    path('social-register',views.regisetSocialUser,name='social-register'),
    path('check-auth',views.checkAuthentication,name='check-auth')
]