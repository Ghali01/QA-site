from django.urls import path
from profiles import views
app_name='profiles'
urlpatterns=[
    path('<int:userID>',views.profilePage,name='profile-page')
]