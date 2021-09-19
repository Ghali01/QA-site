from django.urls import path,re_path
from moderators import views
app_name='moderators'
urlpatterns=[
    path('questions/S/<int:page>',lambda r,page:views.suggestedQuestionsAwait(r,page,"S"),name='suggested-questions-await'),
    path('questions/R/<int:page>',lambda r,page:views.suggestedQuestionsAwait(r,page,"R"),name='suggested-questions-rejected'),
    path('questions/A/<int:page>',lambda r,page:views.suggestedQuestionsAwait(r,page,"A"),name='suggested-questions-accepted'),
    path('review-question/<int:questionID>',views.reviewQuestionPage,name='review-suggested-questions'),
    path('change-suggested-question',views.changeSuggestQuestion,name='change-suggested-question'),
    path('answers/S/<int:page>',lambda r,page:views.suggestedAnswersAwait(r,page,"S"),name='suggested-answers-await'),
    path('answers/A/<int:page>',lambda r,page:views.suggestedAnswersAwait(r,page,"A"),name='suggested-answers-accepted'),
    path('answers/R/<int:page>',lambda r,page:views.suggestedAnswersAwait(r,page,"R"),name='suggested-answers-rejected'),
    path('change-suggested-answers',views.changeSuggestAnswers,name='change-suggested-answers'),
    path('change-suggested-answer',views.changeSuggestAnswer,name='change-suggested-answer'),
]