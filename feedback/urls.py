from django.urls import path
from feedback import views
app_name='feedback'
urlpatterns=[
    path('suggest-category',views.suggestCategory,name='suggest-category'),
    path('suggest-tag',views.suggestTag,name='suggest-tag'),
]