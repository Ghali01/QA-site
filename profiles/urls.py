from django.urls import path
from profiles import views
app_name='profiles'
urlpatterns=[
    path('<int:userID>',views.profilePage,name='profile-page'),
    path('user-questions/<int:userID>',views.userQuestions,name='user-questions'),
    path('see-more-your-questions/<int:userID>/<int:page>',views.seeMoreQuestions,name='see-more-user-questions'),
    path('user-answers/<int:userID>',views.userAnswers,name='user-answers'),
    path('see-more-your-answers/<int:userID>/<int:page>',views.seeMoreAnswers,name='see-more-user-answers'),
]