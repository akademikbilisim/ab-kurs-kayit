#!-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()
urlpatterns = patterns('abkayit.views',
    # Examples:
    # url(r'^$', 'abkayit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^/(?P<menu_id>[1-9]+)/$',"index",name="index"),
    url(r'^$',"index",name="index"),
    url(r'^accounts/',include('userprofile.urls')),
    url(r'^seminer/',include('seminar.urls')),
    url(r'^egitim/',include('training.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
)
urlpatterns += staticfiles_urlpatterns()

