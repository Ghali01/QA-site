from django.urls import path
from profiles import views
app_name='profiles'
urlpatterns=[
    path('<int:userID>',views.profilePage,name='profile-page'),
    path('your-questions/<int:userID>',views.userQuestions,name='user-questions'),
    path('see-more-your-questions/<int:userID>/<int:page>',views.seeMoreQuestions,name='see-more-user-questions'),
]