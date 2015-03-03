from django.conf.urls import patterns, url

from app.movie import views

urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'new_user', views.new_user, name='new_user'),
    url(r'index', views.index, name='index'),
    url(r'^(?P<movie_id>\d+)/$', views.detail, name='detail'),
)
