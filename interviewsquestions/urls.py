
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('',include('content.urls',namespace='content')),
    path('',include('authusers.urls',namespace='authusers')),
    path('',include('misc.urls',namespace='misc')),
    path('dashboard/',include('dashboard.urls',namespace='dashboard',)),
    path('moderators/',include('moderators.urls',namespace='moderators')),
    path('profile/',include('profiles.urls',namespace='profiles')),
    path('feedback/',include('feedback.urls',namespace='feedback')),
    path('polls/',include('polls.urls',namespace='polls')),
    path('i18njs',JavaScriptCatalog.as_view(),name='i18njs'),
    path('admin/', admin.site.urls),


]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
handler404='content.views.error404'