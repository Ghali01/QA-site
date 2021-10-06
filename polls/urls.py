from django.urls import path
from polls import views
app_name='polls'
urlpatterns=[ 
    path('<int:pollID>',views.poll,name='poll-page')
]