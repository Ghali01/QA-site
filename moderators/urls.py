from django.urls import path
from .views import questions as questionsViews ,answers as answersViews,edits as editsViews
app_name='moderators'
urlpatterns=[
    path('questions/S/<int:page>',lambda r,page:questionsViews.suggestedQuestionsAwait(r,page,"S"),name='suggested-questions-await'),
    path('questions/R/<int:page>',lambda r,page:questionsViews.suggestedQuestionsAwait(r,page,"R"),name='suggested-questions-rejected'),
    path('questions/A/<int:page>',lambda r,page:questionsViews.suggestedQuestionsAwait(r,page,"A"),name='suggested-questions-accepted'),
    path('review-question/<int:questionID>',questionsViews.reviewQuestionPage,name='review-suggested-questions'),
    path('change-suggested-question',questionsViews.changeSuggestQuestion,name='change-suggested-question'),
    path('answers/S/<int:page>',lambda r,page:answersViews.suggestedAnswersAwait(r,page,"S"),name='suggested-answers-await'),
    path('answers/A/<int:page>',lambda r,page:answersViews.suggestedAnswersAwait(r,page,"A"),name='suggested-answers-accepted'),
    path('answers/R/<int:page>',lambda r,page:answersViews.suggestedAnswersAwait(r,page,"R"),name='suggested-answers-rejected'),
    path('change-suggested-answers',answersViews.changeSuggestAnswers,name='change-suggested-answers'),
    path('change-suggested-answer',answersViews.changeSuggestAnswer,name='change-suggested-answer'),
    path('edits/S/<int:page>',lambda r,page:editsViews.suggestedEditsAwait(r,page,"S"),name='suggested-edits-await'),
    path('edits/A/<int:page>',lambda r,page:editsViews.suggestedEditsAccepted(r,page,"A"),name='suggested-edits-accepted'),
    path('edits/R/<int:page>',lambda r,page:editsViews.suggestedEditsAwait(r,page,"R"),name='suggested-edits-rejected'),
    path('review-edit/<int:editID>',editsViews.reviewEdit,name='review-edit'),
    path('change-suggested-edit',editsViews.changeSuggestedEditStatus,name='change-suggested-edit')
   ]