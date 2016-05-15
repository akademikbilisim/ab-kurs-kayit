**ab-kurs-kayit**
=================

kurs kayıt ve izleme araçları

**Gereksinimler**

- Python 2.7
- python-devel

- Postgresql 9.2
- postgresql-server
- postgresql-contrib



**Sanal Ortama Kurulum**
Sanal ortam oluşturma ve aktifleştirme:

    virtualenv env
    source env/bin/activate

Gerekli paketlerin sanal ortama kurulması:

    pip install django==1.8.13
    pip install django-settings-context-processor
    pip install psycopg2
    pip install django-ckeditor
    pip install django-country
    pip install pysimplesoap
    pip install django-longerusernameandemail



**Yapılandırma**
Uygulama yapılandırma dosyası abkayit/settings.py dosyasında yer almaktadır. Ancak veritabanı bağlantı bilgileri ile django *SECRET_KEY* bilgisi abkayit/abkayit.config.example dosyasındaki formata benzer bir formatta ayrı bir yapılandırma dosyasında tutulmalıdır. Bu ayrı yapılandırma dosyasındaki bilgileri kullanabilmek için içeriğini doğru bir şekilde doldurulmalıdır ve bu yapılandırma dosyasının sistemdeki yolunu abkayit/settings.py dosyasında *COMMON_CONFIG_FILE* değişkeninde belirtilmelidir.


Uygulamanın menüleri ve menülerin referans verdiği sayfalar dinamik bir şekilde oluşturulmaktadır. Bu nedenle menülerin oluşturulması ve içeriğinin yönetici panelinden(django admin sayfası) girilmesi gerekmektedir. Uygulamayı kullanacak kullanıcıların sisteme kaydolması için de Katılım/Kayıt şeklinde bir menü oluşturulması ve içeriğinde kayıt sayfasına yönlendirecek javascript kodunun konulması gerekmektedirYani menülerden biri Katılım/Kayıt menüsü olmalı ve içeriği de aşağıdaki javascript olmalı:

    <script>
         window.location="/accounts/subscribe"
    </script>

Apache ile kullanmak icin gereksinimler:

-- apache2

-- mod_wsgi

-- mod_ssl


**Katkı Verme**

*git ve github kullanımı*

Yapılacak herhangi bir geliştirmenin(bug, yeni bir özellik) github’ta issue’su olmalı. Yoksa açılmalı
Github’ta açılacak işler etiketlenmeli, bir işe birden fazla etiket eklenebilir
Etiketler şunlar olabilir:

    DOING
    DONE
    WONFIX
    BUG
    ENHANCEMENT
    HELP WANTED
    DUPLICATE
    SERVER
    DOCS
    REFACTORING

Şuanda varolan işler burada açılmaktadır ve buradaki işlere göre geliştirme yapılmaktadır:

    https://github.com/akademikbilisim/ab-kurs-kayit/issues

Eğer bir iş bug ise `BUG` etiketi eklenir, yeni bir özellik veya ister ise `ENHANCEMENT` etiketi eklenir. Belge yazmak ile ilgiliyse `DOCS` eklenir. Uygulamanın koşacağı sunucu ile ilgili bir iş yapılacaksa `SERVER` etiketi eklenir.

Bir bug çözüleceği zaman bug’a sebep olan branch’tan kod dallanır. Dal ismi öneri olarak dallandığı dal ile issue numarasının birleşiminden oluşabilir. Örneğin develop branch’inde varolan bir bug ile ilgili 23 numaralı issue açılsın. Geliştirme `develop` branch’inden dallanılarak *develop_23* diye branch açılarak yapılır. Geliştirme bittikten sonra `develop` branch’i için pull request gönderilir.

Yeni bir özellik ekleneceği zaman master branch’ten yeni dal ayrılır ve geliştirme yapılır. Ayrılacak dalın ismi de master_${issue_number} olabilir. Yapılacak geliştirmeler merge edilmek üzere pull request olarak gönderilir.
Commit mesajları okunaklı yaptığı işi özetleyen nitelikte olmalı ve iş numarasına referans verilmeli.
Commitler atomik olmalı ve biir commit birden fazla işi içermemeli. 
Kullanılacak ek paketler mutlaka `README`’de belirtilmeli


*kod geliştirme*

 - Yazılan kodlar PEP8 standartına uygun olmalı 
 - Mümkün olduğunca sınıf veya metotlara document string kullanılmalıdır 
 - Kodlar hatalara karşı önlem alacak şekilde yazılmalı ve hata olduğunda veya sistemde ne yapıldığına dair fikir edinmek amaçlı mümkün olduğunca log eklenmelidir 
 - Değişken isimleri anlamlı olmalıdır.