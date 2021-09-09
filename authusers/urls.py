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
    path('facebook-register',views.addFacebookUser,name='facebok-register'),
    path('google-login',views.googelLogin,name='google-login'),
    path('google-register',views.addGoogleUser,name='google-register'),
]