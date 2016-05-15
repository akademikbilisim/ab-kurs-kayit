#!-*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('userprofile.views',
                       # register,login,logout
                       url(r'^subscribe', 'subscribe', name="subscribe"),
                       url(r'^profile', 'profile', name="profile"),
                       url(r'^accommodations/(?P<usertype>[a-zA-Z]+)/(?P<gender>[a-zA-Z]+)', 'accommodations', name="accommodations"),
                       url(r'^logout', 'logout', name="logout"),

                       # email verification
                       url(r'^active/done/(?P<key>\w+)/$', 'active', name="active"),
                       url(r'^active/resend/$', 'active_resend', name="active_resend"),

                       # for admins
                       url(r'^allusers', 'all_users', name="all_users"),
                       url(r'^alltrainers', 'all_trainers', name="all_trainers"),

                       # for instructor
                       url(r'^trainer/information', 'trainer_information', name="trainer_information"),

                       # instructor for trainess
                       url(r'^savenote', 'save_note', name="save_note"),

                       # password reset
                       url(r"^password/reset/$", 'password_reset', name="account_reset_password"),
                       url(r"^password/reset/key/$", 'password_reset_key', name="account_reset_password_key"),
                       url(r'^password/reset/key/(?P<key>\w+)/$', 'password_reset_key_done', name="account_reset_password_key_done"),
                       )
