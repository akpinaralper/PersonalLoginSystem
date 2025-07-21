# PersonalLoginSystem
PersonelGirişTakipSistemi


Proje Hakkında
Bu uygulama, küçük ve orta ölçekli işletmelerin personel verilerini ve günlük giriş/çıkış kayıtlarını kolayca yönetmelerini sağlar. Güvenli giriş mekanizmaları, kullanıcı dostu arayüzler ve temel raporlama özellikleriyle donatılmıştır.

Özellikler
Yönetici Paneli
Güvenli Yönetici Girişi: Şifrelenmiş parola ile güvenli giriş.

Genel Bakış (Dashboard): Toplam personel ve admin sayılarının gösterildiği özet panel.

Admin Yönetimi: Yeni admin hesapları ekleme, mevcut admin bilgilerini (kullanıcı adı, e-posta, şifre) güncelleme ve silme.

Personel Yönetimi: Yeni personel kayıtları ekleme, mevcut personel bilgilerini (ad, soyad, departman, e-posta, telefon, profil fotoğrafı) güncelleme ve silme.

Yoklama Takibi: Tüm personel için yoklama kayıtlarını tarih ve saat detaylarıyla görüntüleme.

Raporlama:

Yoklama listesini Excel dosyası olarak indirme.

Günlük yoklama raporunu e-posta ile gönderme.

Personel Paneli
Güvenli Personel Girişi: Ad, soyad ve e-posta ile giriş yaparak e-posta adresine gönderilen doğrulama kodu ile kimlik doğrulama.

Profil Görüntüleme: Kendi personel bilgilerini (ad, soyad, e-posta, departman, telefon, son giriş tarihi/saati) ve giriş geçmişini görüntüleme.

Profil Güncelleme: Vesikalık fotoğraf yükleyerek profilini güncelleme.

Yoklama İşlemi: Tek tıklama ile işe giriş/çıkış kaydı oluşturma. Sistem, aynı gün içinde birden fazla giriş yapılmasını engeller.

Kullanılan Teknolojiler
Backend: Python (Flask Framework)

Veritabanı: SQLite3

Önyüz: HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons

Şifreleme: werkzeug.security (Parola hashleme için)

E-posta Entegrasyonu: Flask-Mail (Doğrulama kodları ve rapor gönderimi için)

Veri Dışa Aktarımı: csv modülü (Excel uyumlu CSV oluşturma için)

Kurulum ve Çalıştırma
Önkoşullar
Python 3.x

pip (Python paket yöneticisi)

Adımlar
Projeyi Klonlayın:

Bash

git clone <proje-repo-adresi>
cd personel-bilgi-sistemi
Sanal Ortam Oluşturun ve Aktif Edin (Önerilir):

Bash

python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
Gerekli Kütüphaneleri Yükleyin:

Bash

pip install Flask Flask-Mail Werkzeug
Veritabanını Oluşturun:
Projenin temel veritabanı yapısını ve başlangıç admin verisini oluşturmak için veritabani_olustur.py ve ardından tablo_duzelt.py veya tablo_guncelle.py dosyalarını çalıştırın.

Bash

python veritabani_olustur.py
python tablo_guncelle.py # veya python tablo_duzelt.py
Not: tablo_duzelt.py aynı zamanda varsayılan admin kullanıcısını (admin / 1234) sıfırlar ve e-postasını günceller. tablo_guncelle.py ise sadece eksik sütunları ekler.

E-posta Ayarlarını Yapılandırın:
app.py dosyasında mail ayarlarını kendi Gmail hesabınızın uygulama şifresi ile güncelleyin.

Python

app.config['MAIL_USERNAME'] = 'sizin_gmail_adresiniz@gmail.com'
app.config['MAIL_PASSWORD'] = 'sizin_uygulama_sifreniz' # Gmail Uygulama Şifresi
Not: Gmail için uygulama şifresi oluşturmanız gerekebilir. Google Destek sayfasından bilgi alabilirsiniz.

Uygulamayı Çalıştırın:

Bash

python app.py
Tarayıcınızda Açın:
Uygulama varsayılan olarak http://127.0.0.1:5000/ adresinde çalışacaktır.

Kullanım
Uygulamayı başlattıktan sonra ana sayfa sizi giriş türü seçimine yönlendirecektir: Personel Girişi veya Admin Girişi.

Admin Girişi için varsayılan kullanıcı adı admin ve şifre 1234'tür (eğer tablo_duzelt.py çalıştırıldıysa).

Personel Girişi için sisteme kayıtlı bir personelin ad, soyad ve e-posta bilgilerini girerek mailinize gelen doğrulama kodunu kullanmanız gerekmektedir.

Veritabanı Şeması
Proje, personel.db SQLite veritabanında aşağıdaki tabloları kullanır:

admin Tablosu
Sütun Adı	Türü	Açıklama
id	INTEGER	Birincil Anahtar, Otomatik Artan
username	TEXT	Yönetici kullanıcı adı (Benzersiz)
password	TEXT	Hashlenmiş parola
email	TEXT	Yönetici e-posta adresi

E-Tablolar'a aktar
personel Tablosu
Sütun Adı	Türü	Açıklama
id	INTEGER	Birincil Anahtar, Otomatik Artan
ad	TEXT	Personelin adı
soyad	TEXT	Personelin soyadı
departman	TEXT	Personelin departmanı
email	TEXT	Personelin e-posta adresi (Benzersiz)
telefon	TEXT	Personelin telefon numarası
son_giris_tarihi	TEXT	Son giriş yaptığı tarih
son_giris_saati	TEXT	Son giriş yaptığı saat
profil_foto	TEXT	Profil fotoğrafının dosya yolu

E-Tablolar'a aktar
yoklama Tablosu
Sütun Adı	Türü	Açıklama
id	INTEGER	Birincil Anahtar, Otomatik Artan
email	TEXT	Giriş yapan personelin e-postası
tarih	TEXT	Giriş tarihi
saat	TEXT	Giriş saati

E-Tablolar'a aktar





