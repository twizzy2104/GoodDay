from django.conf.urls import url
from enjoy_app import views

app_name = 'enjoy_app'

urlpatterns = [
    url(r'^meteo/$',views.meteo,name='meteo'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^registration/$',views.registration,name='registration'),
    url(r'^horoscope/$',views.horoscope,name='horoscope'),
    url(r'^transports/$',views.transports,name='transports'),
    url(r'^news/$',views.news,name='news'),
    url(r'^user_logout/$',views.user_logout,name='user_logout'),
    url(r'^index/$',views.index,name='index'),
    url(r'^transports/rerc/$',views.rerc,name='rerc'),
    url(r'^transports/rera/$',views.rera,name='rera'),
    url(r'^transports/m14/$',views.m14,name='m14'),
    url(r'^accueil/$',views.accueil,name='accueil'),


]
