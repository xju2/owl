from django.conf.urls import patterns, url

from app.movie import views

urlpatterns = patterns('',
    url(r'index', views.index, name='index'),
    url(r'^(?P<movie_id>\d+)/$', views.detail, name='detail'),
)
