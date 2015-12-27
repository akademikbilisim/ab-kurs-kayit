#!-*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('userprofile.views',
    #register,login,logout
    url(r'^kayit', 'subscribe', name="subscribe"),
    url(r'^profil', 'createprofile', name="createprofile"),
    url(r'^logout', 'logout', name="logout"),

    #email verification
    url(r'^active/done/(?P<key>\w+)/$', 'active', name="active"),
    url(r'^active/resend/$', 'active_resend', name="active_resend"),

    # for admins
    url(r'^tumkullanicilar', 'alluserview', name="alluser"),

    # password reset
    url(r"^password/reset/$", 'password_reset', name="account_reset_password"),
    url(r"^password/reset/key/$", 'password_reset_key', name="account_reset_password_key"),
	url(r'^password/reset/key/(?P<key>\w+)/$', 'password_reset_key_done', name="account_reset_password_key_done"),
)
