from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.account import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^movie/', include('app.movie.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^account/', include('app.account.urls')),

)
