ab-kurs-kayit
=============

Akademik Bilişim Konferansı Öncesi kurs kayıt ve izleme araçları

Gereksinimler:
- Django 1.8.13

- Python 2.7

- python-devel

- Postgresql 9.2

- postgresql-server

- postgresql-contrib

- django-settings-context-processor

- postgresql_psycopg2

-  django-ckeditor

- django-country

- pysimplesoap

- longerusernameandemail

- python-crontab 2.0.2

Abkayit / kamp yazılımı ilk kurulum aşamasında dikkat edilmesi gerekenler:

*** Yapilandirma dosyasi:
- login yetkisi olan bir kullanıcı ile  db oluşurulmalı ve DB bölümünde bu bilgiler belirtilmeli:
[DB]
host: 127.0.0.1
port: 5432
database: veritabaninin adi
dbuser: veritabaninin owner'ı (login yetkisi olmalı)
pass: db parola

- [DJANGO] sekmesi altında random karakterlerden oluşan uygulamanın güvenliği için kullanılan secret_key parametresi

[DJANGO]
secret_key: rastgele oluşturulmuş karakterler


*** settings.py içerisinde:

COMMON_CONFIG_FILE: Yapilandirma dosyasının yolu
EMAIL_FROM_ADDRESS: Sistemden gönderilecek maillerin hangi from adresinden gönderileceği
PREFERENCE_LIMIT: Kurs tercih limiti
ADDITION_PREFERENCE_LIMIT: Ek tercih limiti (ek tercih hakkı verilmeyecekse 0 olmalı.)
ACCOMODATION_PREFERENCE_LIMIT: Konaklama tercih limiti
TRANSPORTATION: Bu değişken eğitmenlerin ek bilgilerinde kullanılıyor. etkinliğe ulaşım seçenekleri
REQUIRE_TRAINESS_APPROVE: Katılımcılar kabul edildikten sonra tekrar geleceği teyit ettirilecek mi? true: katılımcı onayı gerekiyor false: gerekmiyor

*** Admin panelden yapılması gerekenler:

- Sites bölümünden yeni bir site eklemek aktifleştirmek. Siteyi eklerken etkinliğin adı, yılı, url'i,is_active=True, başvuru başlangıç bitiş, etkinlik başlangıç bitiş tarihleri belirtilmeli.
Ayrıca yine site eklerken tercih limiti kadar Kabul tarihi eklemek gerekiyor.
Kabul tarihi eklerken başlangıç ve bitiş tarihi, tercih sırası, For instuctor = True olursa eğitmenler için kabul tarihi, For Trainess =True olursa katılımcılardan geleceklerine dair teyit alınma tarihidir
REQUIRE_TRAINESS_APPROVE = False ise For Trainess =True olan bir Kabul tarihi olmamalı.
- Menüler kısmında solda navigation bar'da listelenecek butonlar belirlenir ve bu menülerin içerikleri. Her bir menü için sırayı belirtmek gerekiyor Menülerin html içerikleri "Contents" kısmında kaynak butonuna tıklanarak yapılır.
Sadece bir view's yönlendirme yapılacaksa: Örneğin katılım kayit için şöyle bir html olmalı:<script type="text/javascript">window.location.href="/accounts/kayit"</script> 

*** Sistemden gönderilen e-postalar:
E-mail template'i admin arayüzünden eklenebilir ve şu bileşenlerden oluşur:
operation_name: hangi islemden sonra gönderilecek ise o işlemin ismi. Bu isimler sabittir. Şunlardan biri olmalı:
		send_activation_key: kullanıcı sisteme ilk kayıt olduğunda gönderilen aktivasyon maili
 		send_reset_password_key: parola sıfırlama adımında anahtarın gönderildiği mail,
		preference_saved: tercihler kaydedildiğinde gönderilen e-posta
		inform_trainers_about_changes: bir kullanıcı öncelikli bir tercihine seçilirse ve daha önceden daha az öncelikli bir kursa seçilmişse bu kursun eğitmenlerine gönderilen bilgilendirme maili
                inform_about_changes: bir kursta bir eğitmen değişiklik yaptıysa diğer eğitmenlere gönderilecek mail
subject: mailin konusu
body_html: django template dilinde olmalı aşağıda örnekleri var.
site: e-postanın kullanılacaği etkinlik
Aşağıdaki örnek içeriklere göre bu şablonlar db'de oluşturulmalı

*** İşlemlere göre e-postanın içerikleri:
*** send_activation_key ***(signals.py)

<html>
<body>
<div>
<p>
Merhaba {{user.first_name}} {{user.last_name}},<br><br>

Akademik Bilişim kayıt sistemine hoşgeldiniz.<br>

Bu ileti aşağıdaki hesabın başarılı bir şekilde oluştuğunu doğrular.<br><br>
<b>Kayıt No : {{user.id}}</b><br>
<b>E-posta : {{user.username}}</b><br><br>

Hesabınız ile ilgili işlemlere devam edebilmek için aşağıdaki linke tıklayarak hesabınızı aktif etmelisiniz.<br>

{{domain}}/accounts/active/done/{{activation_key}}
</p>
</body>
</html>

send_confirm_subject

{{ site.name }} {{ site.year }}


*** send_reset_password_key ***
<html>
<body>
Merhaba {{user.first_name}} {{user.last_name}},

Akademik Bilisim kayit sisteminde hesabınızın parolasını sıfırlamak için aşağıdaki bağlantıyı kullanabilirsiniz.

{{domain}}/accounts/password/reset/key/{{activation_key}}
</body>
</html>

subject:
{{ site.name }} {{ site.year }} Parola Sıfırlama

*** preference_saved *** (training.tutils.py)
Merhaba<br><br>

Tercihleriniz başarıyla alınmıştır.<br>
Kurs tercihleriniz:<br>
{% for cp in course_prefs %}
{{ cp.preference_order }}. tercih: {{ cp.course.no }} - {{ cp.course.name }}<br>
{% endfor %}

{{ site.name }} - {{ site.year }}<br>

subject:
{{ site.name }} {{ site.year }} - Kurs Tercihi


*** inform_trainers_about_changes *** (training.tutils.py) to: data['course'].trainer.all().values_list('user__username', flat=True)
Merhaba,<br>
<br>
{{ changedpref.course.no }} numaralı {{ changedpref.course.name }} kursunuza kabul ettiğiniz {{ changedpref.trainess.user }} kullanıcısı <br>
{{ approvedpref.preference_order }}. tercihi olan {{ approvedpref.course.name }} kursuna kabul edilmiştir.<br>
<br>
Yapılan değişiklikleri görmek için https://{{ site.url }}/egitim/controlpanel adresini ziyaret ediniz.<br>
<br>
{{ site.name }} - {{ site.year }}<br>

Subject:
{{ site.name }} {{ site.year }} - Güncelleme Bilgilendirmesi

*** inform_about_changes *** 

Merhaba,<br>
<br>
{{ course.no }} numaralı kursta  güncelleme yapılmıştır.<br>
<br>
Yapılan değişiklikleri görmek için https://{{ site.url }}/egitim/controlpanel adresini ziyaret ediniz.<br>
<br>
{{ site.name }} - {{ site.year }}<br>

Subject:
{{ site.name }} {{ site.year }} - Güncelleme Bilgilendirmesi


*** notice_for_canceled_prefs *** training.views.py

Merhaba,<br><br>

Aşağıdaki bilgileri verilen katılımcı "Tüm Başvurularımı İptal Et" seçeneği ile tercihlerini iptal etti.<br><br>

Katılımcı: {{trainess_course_record.trainess.user.username}}<br>
Kurs: {{trainess_course_record.course.no}} - {{trainess_course_record.course.name}}<br>
Tercih Sırası: {{trainess_course_record.preference_order}}<br>

subject:
{{ site.name }} {{ site.year }} - Kurs Tercih İptal Bilgilendirmesi

*** send_consent_email ***

Merhaba,<br><br>

{{ approvedpref.preference_order }}. tercihiniz olan {{ approvedpref.course.no }} nolu {{ approvedpref.course.name }}<br>
kursuna başvurunuz kabul edilmiştir.

subject:
{{ site.name }} {{ site.year }} - Kabul Edilen Tercihiniz

*** not_approved_trainess_after_approval_period_ends ***

Merhaba,<br><br>

Kurslara kabul dönemi bitmiş olup başvurularınıza kabul edilmediniz ancak kurs başlangıç tarihine kadar kabul edilme şansınız hala devam ediyor.<br><br>
Takip etmeye devam edin.<br><br>

Bilginize,<br>

subject:
{{ site.name }} {{ site.year }} - Tercihleriniz Hakkında

*** not_approved_trainess_eventstardate ***

Merhaba,<br><br>

Başvurularınız kabul edilmemiştir. Bir sonraki etkinlikte görüşmek dileğiyle<br><br>


subject:
{{ site.name }} {{ site.year }} - Tercihleriniz Hakkında