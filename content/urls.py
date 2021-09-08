from django.urls import path
from .views import index
app_name='content'
urlpatterns=[
    path('',index,name='index'),
    path('<int:categoryID>',index,name='index'),
    
]