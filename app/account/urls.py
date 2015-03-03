__author__ = 'xju'
from django.conf.urls import patterns, url

from app.account import views

urlpatterns = patterns('',
        url(r'^sign_in/$',       views.sign_in,          name='sign_in'),
        url(r'^do_sign_in/$',    views.do_sign_in,       name='do_sign_in'),
        url(r'^sign_up/$',       views.sign_up,          name='sign_up'),
        url(r'^do_sign_up/$',    views.do_sign_up,       name='do_sign_up'),
        url(r'^change_pwd/$',    views.change_pwd,       name='change_pwd'),
        url(r'^do_change_pwd/$', views.do_change_pwd,    name='do_change_pwd'),
        url(r'^sign_out/$',      views.sign_out,         name='sign_out'),
)