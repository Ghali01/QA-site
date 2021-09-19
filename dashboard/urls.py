from django.urls import path
from dashboard.views import main as mainViews,categories as categoriesViews,tags as tagsViews,users as usersViews
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
]