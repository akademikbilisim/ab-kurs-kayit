from django.conf.urls import patterns, url

urlpatterns = patterns('userprofile.views',
    url(r'^kayit', 'subscribe', name="subscribe"),
    url(r'^login', 'loginview', name="login"),
    url(r'^logout', 'logout', name="logout"),
)
