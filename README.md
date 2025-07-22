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
Herhangi bir sorunuz veya geri bildiriminiz varsa, GitHub Issues üzerinden bana ulaşabilirsiniz.
```
🙌 Katkıda Bulunmak
```bash
Katkılar her zaman açıktır! Yeni özellikler eklemek, hataları düzeltmek veya performansı artırmak için çekme istekleri (Pull Request) göndermekten çekinmeyin.
```

### EKRAN GÖRÜNTÜLERİ
<img width="1916" height="876" alt="ana_giris" src="https://github.com/user-attachments/assets/0a4b1815-e3b0-42fa-86f2-1d2ebd4b6360" />

<img width="1918" height="876" alt="admin_giris" src="https://github.com/user-attachments/assets/c59e706f-5199-42b8-a796-a0b2b8757aba" />

<img width="1906" height="876" alt="admin_panel" src="https://github.com/user-attachments/assets/83992020-dfa0-4597-9db3-65c47a53f813" />

<img width="1903" height="883" alt="admin_ekleme" src="https://github.com/user-attachments/assets/22ec62af-e891-4920-b146-9fc43afc3b2c" />

<img width="1918" height="878" alt="personel_ekleme" src="https://github.com/user-attachments/assets/970ad483-6331-41ec-bc03-e9212ae22264" />

<img width="1920" height="880" alt="admin_guncelle" src="https://github.com/user-attachments/assets/b3ee1140-c11e-4480-9272-758d42e9b234" />

<img width="1900" height="878" alt="yoklama_ekrani" src="https://github.com/user-attachments/assets/d3b457e0-2e0f-47e8-9c3d-0526d4293baa" />

<img width="1917" height="876" alt="personel_guncelleme" src="https://github.com/user-attachments/assets/322c3c8e-9e92-4074-b4cf-294e1167eb85" />

<img width="1910" height="872" alt="raporonizleme" src="https://github.com/user-attachments/assets/81018bf7-c278-41bf-b3cc-89f5e78460e6" />

<img width="1920" height="881" alt="personel_girisi" src="https://github.com/user-attachments/assets/c423ffb8-681a-4f50-b977-7ef4bb11a229" />

<img width="1920" height="872" alt="personel_kod_ekrani" src="https://github.com/user-attachments/assets/2c1bc7b9-14dc-4cf7-803a-11344412af86" />

<img width="1918" height="877" alt="is_onay_ekrani" src="https://github.com/user-attachments/assets/6a3d4836-c6df-489e-9a00-b7a5a11f869b" />

<img width="1917" height="877" alt="motivasyon_ekrani" src="https://github.com/user-attachments/assets/745b3758-03ca-412c-9903-96cb4bc63536" />

<img width="1381" height="868" alt="mail_rapor" src="https://github.com/user-attachments/assets/542e63d5-51b2-4735-9e8a-816797aea3de" />

```bash
🚀 Hazırlayan: [Alper Akpınar] 
🏢 Proje Versiyonu: 1.0.0
📅 İlk Yayın Tarihi: 2025
```




