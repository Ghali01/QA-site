from django.urls import path
from .views import addAnswer, addCommentToPost, addQuestionPage, allPostComment, index, postVotes, questionPage, seeMoreQueIndex, similarQuestions, suggestPostEdit
app_name='content'
urlpatterns=[
    path('',index,name='index'),
    path('<int:categoryID>',index,name='index-with-cate'),
    path('see-more/<int:page>',seeMoreQueIndex,name='see-more-index'),
    path('see-more/<int:page>/<int:categoryID>',seeMoreQueIndex,name='see-more-index-with-cate'),
    path('add-question',addQuestionPage,name='add-question'),
    path('question/<int:questionID>',questionPage,name='question-page'),
    path('post-vote',postVotes,name='post-vote'),
    path('add-answer',addAnswer,name='add-answer'),
    path('similar-questions/<int:page>',similarQuestions,name='similar-questions'),
    path('add-comment',addCommentToPost,name='add-comment'),
    path('all-comment',allPostComment,name='all-comment'),
    path('suggets-edit/<int:postID>',suggestPostEdit,name='suggest-post-edit')
]