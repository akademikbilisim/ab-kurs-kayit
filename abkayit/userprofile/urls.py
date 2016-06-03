#!-*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('userprofile.views',
                       # register,login,logout
                       url(r'^kayit', 'subscribe', name="subscribe"),
                       url(r'^profil', 'createprofile', name="createprofile"),
                       url(r'^getaccomodations/(?P<usertype>[a-zA-Z]+)/(?P<gender>[a-zA-Z]+)', 'getaccomodations',
                           name="getaccomodations"),
                       url(r'^logout', 'logout', name="logout"),

                       # email verification
                       url(r'^active/done/(?P<key>\w+)/$', 'active', name="active"),
                       url(r'^active/resend/$', 'active_resend', name="active_resend"),

                       # for admins
                       url(r'^tumkullanicilar', 'alluserview', name="alluser"),
                       url(r'^tumegitmenler', 'get_all_trainers_view', name="alltrainers"),

                       # for instructor
                       url(r'^egitmen/bilgi', 'instructor_information', name="instructor_information"),
                       url(r'^showuser/(?P<userid>[0-9]+)/(?P<courserecordid>[0-9]+)', 'showuserprofile', name="showuserprofile"),

                       # instructor for trainess
                       url(r'^savenote', 'save_note', name="save_note"),

                       # password reset
                       url(r"^password/reset/$", 'password_reset', name="account_reset_password"),
                       url(r"^password/reset/key/$", 'password_reset_key', name="account_reset_password_key"),
                       url(r'^password/reset/key/(?P<key>\w+)/$', 'password_reset_key_done',
                           name="account_reset_password_key_done"),
                       )
