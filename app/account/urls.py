__author__ = 'xju'
from django.conf.urls import patterns, url
from app.account import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^index/$', views.index, name='index'),
        url(r'^tologin/$', views.tologin, name='tologin'),
        url(r'^tosignup/$', views.tosignup, name='tosignup'),
        url(r'^login/$', views.login, name='login'),
        url(r'^tochangepwd/$', views.to_change_pwd,name='to_change_pwd'),
        url(r'^changepwd/$', views.change_pwd, name='change_pwd'),
        url(r'^logout/$', views.logout,name='logout'),
)