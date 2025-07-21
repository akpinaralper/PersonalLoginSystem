# 🧑‍💼 Personel Giriş Takip Sistemi

![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite]( https://img.shields.io/badge/SQLite-00385C?style=for-the-badge&logo=sqlite&logoColor=white)
![Python]( https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bootstrap]( https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

> **Personel Giriş Takip Sistemi**, Flask ve SQLite kullanılarak geliştirilmiş bir web tabanlı personel devam takip uygulamasıdır. Yönetici paneli, e-posta doğrulamalı giriş, yoklama kaydı ve raporlama gibi birçok özellik sunar.

---

## 🌟 Özellikler

### 👑 Yönetici Paneli
- **🔑 Güvenli Giriş:** Yöneticiler için parola korumalı özel giriş ekranı.
- **👥 Personel Yönetimi (CRUD):**
  - Yeni personel ekleme
  - Personel bilgilerini güncelleme
  - Personel silme
- **🛡️ Yetki Bazlı Admin Yönetimi:** Super Admin yeni yöneticiler ekleyebilir veya mevcutları silebilir.
- **📊 Devam Takibi ve Raporlama:**
  - Giriş kayıtlarını tarih ve saate göre görüntüleme
  - Yoklama verilerini `.csv` formatında dışa aktarma
  - Günlük yoklama raporunu tüm yöneticilere e-posta ile gönderme

### 👤 Personel Arayüzü
- **🔐 E-posta ile İki Aşamalı Giriş:** Personel, sisteme kayıtlı bilgilerle giriş yaptıktan sonra e-posta ile gelen 6 haneli kodla doğrulama yapar.
- **✅ Tek Tıkla Yoklama:** Başarılı doğrulama sonrası "İŞE GELDİM" butonu ile devam kaydı yapılır.
- **💖 Motivasyon Ekranı:** Her başarılı girişte kullanıcıya pozitif karşılama mesajı ve motivasyonel bir söz gösterilir.

---

## 🛠️ Kullanılan Teknolojiler

| Kategori         | Kullanılanlar                                                                 |
|------------------|-------------------------------------------------------------------------------|
| Backend          | Python (Flask Framework)                                                      |
| Veritabanı       | SQLite3                                                                       |
| Önyüz            | HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons                                   |
| Şifreleme        | `werkzeug.security` (Parola hashleme için)                                    |
| E-posta Entegrasyonu | Flask-Mail (Doğrulama kodları ve rapor gönderimi için)                 |
| CSV Dışa Aktarım | `csv` modülü                                                                  |

---

## 📦 Kurulum ve Çalıştırma

### 🧰 Gereksinimler

- Python 3.x
- pip (Python paket yöneticisi)

---

##  📥 1. Projeyi Klonlayın

```bash
git clone <proje-repo-adresi>
cd PersonelGirişTakipSistemi
````

## 2. Sanal Ortam Oluşturun ve Aktif Edin
```bash
Windows:
python -m venv venv
.\venv\Scripts\activate

macOS/Linux:

python3 -m venv venv
source venv/bin/activate
````


## 📦 3. Gerekli Kütüphaneleri Yükleyin
```bash
pip kullanarak projede kullanılan Python kütüphanelerini yükleyin:

pip install Flask Flask-Mail requests
````

## 4️⃣ Veritabanını Oluşturun
```bash
veritabani_olustur.py script'ini çalıştırarak personel.db dosyasını ve gerekli tabloları oluşturun. Bu script, aynı zamanda varsayılan yönetici hesabını da oluşturur.
python veritabani_olustur.py
python tablo_guncelle.py  # veya tablo_duzelt.py
Not: tablo_duzelt.py varsayılan admin (admin / 1234) hesabını sıfırlar ve e-posta alanını ekler. 
````

## 📨 5. E-posta Ayarlarını Yapılandırın
```bash
app.py dosyasında aşağıdaki satırları kendi Gmail hesabınıza göre güncelleyin:
app.config['MAIL_USERNAME'] = 'sizin_gmail_adresiniz@gmail.com'
app.config['MAIL_PASSWORD'] = 'sizin_uygulama_sifreniz'  # Gmail Uygulama Şifresi
````
## ▶️ 6. Uygulamayı Başlatın
```bash
python app.py
```

## 🌐 7. Tarayıcıda Açın
```bash
Uygulama şu adreste çalışacaktır:
http://127.00.1:5000/
```


📚 Kullanım
```bash
Uygulama başlatıldıktan sonra ana sayfa, giriş türü seçmenizi ister: Personel Girişi veya Admin Girişi .
Admin Girişi: Varsayılan kullanıcı adı admin, şifre 1234 (eğer tablo_duzelt.py çalıştırıldıysa).
Personel Girişi: Sisteme kayıtlı bir personelin ad, soyad ve e-posta bilgileri ile giriş yapabilir. Doğrulama için e-postasına gönderilen 6 haneli kodu girmelidir.
```

📧 İletişim
```bash
Herhangi bir sorunuz veya geri bildiriminiz varsa, GitHub Issues üzerinden bize ulaşabilirsiniz.
```
🙌 Katkıda Bulunmak
```bash
Katkılar her zaman açıktır! Yeni özellikler eklemek, hataları düzeltmek veya performansı artırmak için çekme istekleri (Pull Request) göndermekten çekinmeyin.
```







