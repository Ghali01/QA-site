from os import name
from django.urls import path
from profiles import views
app_name='profiles'
urlpatterns=[
    path('<int:userID>',views.profilePage,name='profile-page'),
    path('user-questions/<int:userID>',views.userQuestions,name='user-questions'),
    path('see-more-your-questions/<int:userID>/<int:page>',views.seeMoreQuestions,name='see-more-user-questions'),
    path('user-answers/<int:userID>',views.userAnswers,name='user-answers'),
    path('see-more-your-answers/<int:userID>/<int:page>',views.seeMoreAnswers,name='see-more-user-answers'),
    path('badges/<int:userID>',views.userBadges,name='badges'),
    path('see-more-badges/<int:page>',views.seeMoreBadges,name='see-more-badges'),
    path('user-followers//<int:userID>',views.userFollowers,name='user-followers'),
    path('see-more-followers/<int:page>',views.seeMoreFollowers,name='see-more-followers'),
    path('favorite-questions/<int:userID>',views.favQuestion,name='favorite-questions'),
    path('see-more-fav-que/<int:page>',views.seeMoreFavQuestion,name='see-more-favorite-questions'),
    path('chang-avatar',views.changeAavatar,name='chang-avatar'),
    path('settings',views.profileSettings,name='user-settings'),
    path('my-tags',views.myTags,name='user-tags'),
    path('image/<int:userID>',views.downloadImagProfile,name='image-profile')
]