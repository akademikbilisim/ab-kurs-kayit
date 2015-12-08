ab-kurs-kayit
=============

Akademik Bilişim Konferansı öncesi kurs kayıt ve izleme araçlar�

Gereksinimler:
-- Django 1.7
-- Python 2.7
-- python-devel
-- Postgresql 9.2
-- postgresql-server
-- postgresql-contrib
-- django-settings-context-processor
-- postgresql_psycopg2
-  django-ckeditor
- django-country
Apache ile kullanmak icin gereksinimler:
-- apache2
-- mod_wsgi
-- mod_ssl
-- site httpd.conf:
(SSL icin ayar)
SSLCertificateFile /etc/httpd/ssl/apache.crt
SSLCertificateKeyFile /etc/httpd/ssl/apache.key
ServerName <server_name>:443
WSGIScriptAlias / /opt/abkayit/abkayit/wsgi.py
WSGIPythonPath /opt/abkayit/

Alias /static/ /opt/abkayit/static/

<Directory /opt/abkayit/static>
Require all granted
</Directory>

<Directory /opt/abkayit/abkayit/>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
RewriteEngine On
RewriteCond %{HTTPS} !=on
RewriteRule ^/?(.*) https://%{SERVER_NAME}/$1 [R,L]
