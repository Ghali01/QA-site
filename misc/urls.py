from django.urls import path
from django.urls.conf import include
from misc import views
app_name='misc'
urlpatterns=[
    path('info',views.InfoPage,name='info-page'),
    path('services',views.servicesPage,name='services-page'),
    path('contact-us',views.contactUS,name='contact-us'),
    path('advertise-with-us',views.advertiseWithUs,name='advertise-with-us'),
] 