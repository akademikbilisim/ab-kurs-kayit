#!-*- coding:utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as authviews


admin.autodiscover()
urlpatterns = patterns('abkayit.views',
                       url(r'^/(?P<menu_id>[1-9]+)/$', "index", name="index"),
                       url(r'^$', "index", name="index"),
                       url(r'^test', "testbeforeapply", name="testbeforeapply"),
                       url(r'^auth/login$', authviews.login, name="authlogin"),
                       url(r'^auth/logout$', "auth_logout", name="authlogout"),
                       url(r'^accounts/', include('userprofile.urls')),
                       url(r'^egitim/', include('training.urls')),
                       url(r'^admin/', include(admin.site.urls), name="admin_entrypoint"),
                       url(r'^survey/', include("surman.urls")),
                       url(r'^ckeditor/', include('ckeditor_uploader.urls')),
                       )
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)