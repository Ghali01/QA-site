
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',include('authusers.urls',namespace='authusers')),
    path('',include('content.urls',namespace='content')),
    path('dashboard/',include('dashboard.urls',namespace='dashboard',)),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)