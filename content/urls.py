from django.urls import path
from .views import addQuestion, addQuestionPage, index
app_name='content'
urlpatterns=[
    path('',index,name='index'),
    path('<int:categoryID>',index,name='index'),
    path('add-question',addQuestionPage,name='add-question'),
    path('submit-que',addQuestion,name='submit-que'),
]