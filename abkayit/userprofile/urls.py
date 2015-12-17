#!-*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('userprofile.views',
	#register,login,logout
    url(r'^kayit', 'subscribe', name="subscribe"),
    url(r'^profil', 'createprofile', name="createprofile"),
    url(r'^login', 'loginview', name="login"),
    url(r'^logout', 'logout', name="logout"),

	#email verification
	url(r'^activate/(?P<key>\w+)/$', 'activate', name="activate"),

    # password reset
    url(r"^password/reset/$", 'password_reset', name="account_reset_password"),
    url(r"^password/reset/key/$", 'password_reset_key', name="account_reset_password_key"),
	url(r'^password/reset/key/(?P<key>\w+)/$', 'password_reset_key_done', name="account_reset_password_key_done"),
)
