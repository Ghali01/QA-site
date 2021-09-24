
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',include('content.urls',namespace='content')),
    path('',include('authusers.urls',namespace='authusers')),
    path('dashboard/',include('dashboard.urls',namespace='dashboard',)),
    path('moderators/',include('moderators.urls',namespace='moderators')),
    path('profile/',include('profiles.urls',namespace='profiles')),
    path('feedback/',include('feedback.urls',namespace='feedback')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)