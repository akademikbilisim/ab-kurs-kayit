from django.conf.urls import patterns, url

urlpatterns = patterns('seminar.views',
    url(r'^yenibasvuru', 'new_seminar', name="newseminar"),
    url(r'^listele', 'list_seminars', name="listseminars"),
	url(r'^duzenle', 'edit_seminar', name="editseminar"),
	url(r'^goster', 'show_seminar', name="showseminar"),
	url(r'^kayit', 'apply_seminar', name="showseminar"),
)
