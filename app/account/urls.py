from django.conf.urls import patterns, url

from app.account.views import *

urlpatterns = patterns('',
        url(r'^sign_in/$',              sign_in,                name='sign_in'),
        url(r'^sign_up/$',              sign_up,                name='sign_up'),
        url(r'^reset_password/$',       reset_password,         name='reset_password'),
        url(r'^sign_out/$',             sign_out,               name='sign_out'),

        url(r'^profile/$',              profile,                name='profile'),
        url(r'^security/$',             security,               name='security'),

)