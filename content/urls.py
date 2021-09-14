from django.urls import path
from .views import addAnswer, addQuestion, addQuestionPage, index, postVotes, questionPage
app_name='content'
urlpatterns=[
    path('',index,name='index'),
    path('<int:categoryID>',index,name='index'),
    path('add-question',addQuestionPage,name='add-question'),
    path('submit-que',addQuestion,name='submit-que'),
    path('question/<int:questionID>',questionPage,name='question-page'),
    path('post-vote',postVotes,name='post-vote'),
    path('add-answer',addAnswer,name='add-answer')
]