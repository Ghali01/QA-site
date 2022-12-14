from django.urls import path
from dashboard.views import main as mainViews,categories as categoriesViews,tags as tagsViews,users as usersViews,questions as questionsViews, Suggestedfeedback as SuggestedfeedbackViews,editsite as editSiteViews,messages as messagesViews,Email as emailTemplateViews,badges as badgesViews,flag as flagViews,polls as pollsViews
app_name='dashboard'
urlpatterns=[
    path('',mainViews.index,name='index'),
    path('login',mainViews.loginPage,name='login'),
    path('logout',mainViews.logout,name='logout'),
    path('categories/<str:language>',categoriesViews.categoriesPage,name='categories'),
    path('add-category',categoriesViews.addCategory,name='add-category'),
    path('delete-category',categoriesViews.deleteCategory,name='delete-category'),
    path('edit-category',categoriesViews.editCategory,name='edit-category'),
    path('tags/<str:language>',tagsViews.tagsPage,name='tags'),
    path('add-tag',tagsViews.addTag,name='add-tag'),
    path('edit-tag',tagsViews.editTag,name='edit-tag'),
    path('delete-tag',tagsViews.deleteTag,name='delete-tag'),
    path('category-tags',tagsViews.tagsCategoryJson,name='category-tags'),
    path('search-tags',tagsViews.tagsSearchJson,name='search-tags'),
    path('users',usersViews.usersPage,name='users'),
    path('search-users',usersViews.searchUsers,name='search-users'),
    path('set-user-perm',usersViews.setUserPermission,name='set-user-perm'),
    path('questions/<int:page>',questionsViews.questions,name='questions'),
    path('del-que',questionsViews.deleteQuestion,name='delete-questison'),
    path('question/<int:questionID>',questionsViews.editQuestion,name='edit-question-page'),
    path('answers/<int:page>',questionsViews.answers,name='all-answers-page'),
    path('answers/<int:page>/<int:questionID>',questionsViews.answers,name='question-answers-page'),
    path('del-ans',questionsViews.deleteAnswer,name='delete-answer'),
    path('edit-answer/<int:answerID>',questionsViews.editAnswer,name='edit-answer-page'),
    path('post-comments/<int:page>/<int:postID>',questionsViews.postComments,name='post-comments'),
    path('del-comment',questionsViews.deleteComment,name='delete-comment'),
    path('edit-comment/<int:commentID>',questionsViews.editComment,name='edit-comment'),
    path('post-logs/<int:postID>',questionsViews.postLogs,name='post-logs'),
    path('review-log/<int:logID>',questionsViews.reviewLog,name='review-log'),
    path('togg-pub-post',questionsViews.toggelPostPublish,name='togg-pub-post'),
    path('prune-user',usersViews.pruneUser,name='prune-user'),
    path('togg-ban-user',usersViews.toggleBanUser,name='toggle-ban-user'),
    path('suggested-categories/<str:language>/<int:page>',SuggestedfeedbackViews.suggestedCategories,name='suggested-categories'),
    path('delete-sug-cate',SuggestedfeedbackViews.deleteSuggestedCategory,name='delete-suggested-category'),
    path('acc-sug-cate/<int:itemID>/<int:page>',SuggestedfeedbackViews.acceptSuggestdCategory,name='accept-suggested-category'),
    path('acc-sug-cate-app',SuggestedfeedbackViews.acceptCategoryAfterApproval,name='accept-suggested-category-approval'),
    path('suggested-tags/<str:language>/<int:page>',SuggestedfeedbackViews.suggestedTags,name='suggested-tags'),
    path('delete-sug-tag',SuggestedfeedbackViews.deleteSuggestedTag,name='delete-suggested-tag'),
    path('acc-sug-tag/<int:itemID>/<int:page>',SuggestedfeedbackViews.acceptSuggestdTag,name='accept-suggested-tag'),
    path('acc-sug-tag-app',SuggestedfeedbackViews.acceptTagAfterApproval,name='accept-suggested-tag-approval'),
    path('edit-info/<str:language>',editSiteViews.editInfoPage,name='edit-info-page'),
    # path('save-info/<str:language>',editSiteViews.saveInfo,name='save-info'),
    path('column/<str:language>/<str:side>',editSiteViews.editColumnPage,name='edit-column'),
    path('del-card/<str:language>/<str:side>',editSiteViews.deleteCard,name='delete-card'),
    path('add-card/<str:language>/<str:side>',editSiteViews.addCardPage,name='add-card-page'),
    path('save-card/<str:language>/<str:side>',editSiteViews.addCard,name='save-card'),
    path('edit-card/<str:language>/<str:side>/<str:cardID>',editSiteViews.editCardPage,name='edit-card-page'),
    path('update-card/<str:language>/<str:side>/<str:cardID>',editSiteViews.updateCard,name='update-card'),
    path('edit-footer/<str:language>',editSiteViews.editFooterPage,name='edit-footer-page'),
    path('save-footer/<str:language>',editSiteViews.saveFooter,name='save-footer'),
    path('edit-header/<str:language>',editSiteViews.editHeaderPage,name='edit-header-page'),
    path('save-header/<str:language>',editSiteViews.saveHeader,name='save-header'),
    path('edit-advertise/<str:language>',editSiteViews.editAdvertisePage,name='edit-advertise-page'),
    path('save-advertise/<str:language>',editSiteViews.saveAdvertise,name='save-advertise'),
    path('delete-advertise-img/<str:language>/<int:imageID>',editSiteViews.deleteAdvertiseImg,name='delete-advertise-img'),
    path('edit-services/<str:language>',editSiteViews.editServicesPage,name='edit-services-page'),
    path('add-service/<str:language>',editSiteViews.addServicePage,name='add-service-page'),
    path('save-service/<str:language>',editSiteViews.addService,name='save-service'),
    path('edit-service/<int:serviceID>',editSiteViews.editServicePage,name='edit-service-page'),
    path('update-service',editSiteViews.updateService,name='update-service'),
    path('delete-service/<str:language>',editSiteViews.deleteService,name='delete-service'),
    path('add-info-item/<str:language>',editSiteViews.addInfoItemPage,name='add-info-item-page'),
    path('save-info-item/<str:language>',editSiteViews.addInfoItem,name='save-info-item'),
    path('edit-info-item/<int:itemID>',editSiteViews.editInfoItemPage,name='edit-info-item-page'),    
    path('update-info-item',editSiteViews.updateInfoItem,name='update-info-item'),
    path('delete-info-item/<str:language>',editSiteViews.deleteInfoItem,name='delete-info-item'),
    path('advertise-messages/<str:language>/<int:page>',messagesViews.advertiseMessage,name='advertise-messages'),
    path('advertise-message/<int:messageID>',messagesViews.showAdverticeMessage,name='advertise-message'),
    path('del-ads-msg/<str:language>/<int:page>',messagesViews.deleteAdverticeMessage,name='delete-advertset-message'),
    path('contact-messages/<str:language>/<int:page>',messagesViews.contactMessage,name='contact-messages'),
    path('contact-message/<int:messageID>',messagesViews.showContactMessage,name='contact-message'),
    path('del-con-msg/<str:language>/<int:page>',messagesViews.deleteContactMessage,name='delete-contact-message'),
    path('templates/<str:language>',emailTemplateViews.TenmplatesPage,name='templates'),
    path('add-template/<str:language>',emailTemplateViews.addTemplatePage,name='add-template'),
    path('save-template',emailTemplateViews.addTemplate,name='save-template'),
    path('del-template',emailTemplateViews.deleteTemplate,name='del-template'),
    path('edit-template/<int:templateID>',emailTemplateViews.editTemplatePage,name='edit-template'),
    path('update-template',emailTemplateViews.updateTemplate,name='update-template'),
    path('email/<str:language>',lambda r,language:emailTemplateViews.sendEmailPage(r,language,-1),name='email-non-temp'),
    path('email/<str:language>/<int:templateID>',emailTemplateViews.sendEmailPage,name='email-page'),
    path('send-email',emailTemplateViews.sendEmail,name='send-email'),
    path('badges/<int:page>',badgesViews.BadgesPage,name='badges-page'),
    path('add-badge',badgesViews.addBadge,name='add-badge'),
    path('del-badge',badgesViews.deleteBadge,name='delete-badge'),
    path('edit-badge/<int:badgeID>',badgesViews.editBadge,name='edit-badge'),
    path('flag-reasons/<str:type>',flagViews.flagReasons,name='flag-reasons'),
    path('add-flag-reason/<str:type>',flagViews.addReason,name='add-flag-reason'),
    path('delete-flag-reason',flagViews.deleteReason,name='delete-flag-reason'),
    path('edit-reason/<int:reasonID>',flagViews.editReason,name='edit-reason'),
    path('flaged-questions/<int:page>',flagViews.flagedQuestions,name='flaged-questions'),
    path('flaged-answers/<int:page>',flagViews.flagedAnswers,name='flaged-answers'),
    path('flaged-users/<int:page>',flagViews.flagedUsers,name='flaged-users'),
    path('remove-reports',flagViews.removeReports,name='remove-reports'),
    path('polls/<int:page>/<str:language>',pollsViews.polls,name='polls'),
    path('add-poll/<str:language>',pollsViews.addPoll,name='add-poll'),
    path('delete-poll',pollsViews.deletePoll,name='delete-poll'),
    path('edit-poll/<int:pollID>',pollsViews.editPoll,name='edit-poll'),
    path('pub-poll',pollsViews.publishPoll,name='pub-poll'),
    path('togg-poll-open',pollsViews.toggPollOpen,name='toggle-poll-open'),
    path('poll-resaults/<int:pollID>',pollsViews.pollResault,name='poll-resaults'),
    path('togg-exam-que',questionsViews.toggExamQuestion,name='toggle-exam-question'),
    path('mark-correct-ans',questionsViews.markCorrectAnswer,name='mark-correct-ans'),
    path('options',mainViews.options,name='options-page'),
    path('restart-server',mainViews.restaratServer,name='restart-server'),
    path('statistics/<str:language>',mainViews.statistics,name='statistics'),
    path('edit-page/<str:page>/<str:language>',editSiteViews.editAuthPage,name='edit-auth-page'),
    path('edit-terms/<str:language>',editSiteViews.editTermsAndPolicy,name='edit-terms')

  ]