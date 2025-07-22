from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from smtplib import SMTP
import sqlite3
import random
from datetime import datetime
import csv
from io import StringIO
from flask import Response
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
app.secret_key = 'gizlianahtar'  # session için gerekli

# Mail ayarları
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'metinarslan2507@gmail.com'
app.config['MAIL_PASSWORD'] = 'dzvqztcbutfuerns'
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']
mail = Mail(app)

# Veritabanı bağlantı fonksiyonu
def get_db_connection():
    conn = sqlite3.connect('personel.db')
    conn.row_factory = sqlite3.Row  # dict gibi erişim için
    return conn

@app.route('/')
def index():
    return render_template('login_select.html')

# Admin Giriş Sayfası
@app.route('/admin_login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        kullanici = request.form['username']
        sifre = request.form['password']
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admin WHERE username = ?', (kullanici,)).fetchone()
        conn.close()
        if admin and check_password_hash(admin['password'], sifre):
            session['logged_in'] = True
            session['username'] = admin['username']
            session['admin_email'] = admin['email']
            session['is_super_admin'] = (admin['username'] == 'admin')
            return redirect(url_for('dashboard'))
        else:
            flash('Hatalı kullanıcı adı veya şifre!')
    return render_template('login.html')

# Ana Sayfa - Personel Listesi
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    personeller = conn.execute('SELECT * FROM personel').fetchall()
    adminler = conn.execute('SELECT * FROM admin').fetchall()
    conn.close()
    return render_template('dashboard.html', personeller=personeller, adminler=adminler)

# Çıkış Yap
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Personel Ekleme Sayfası
@app.route('/add', methods=['GET', 'POST'])
def add_personel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        ad = request.form.get('ad', '').strip()
        soyad = request.form.get('soyad', '').strip()
        departman = request.form.get('departman', '').strip()
        email = request.form.get('email', '').strip()
        telefon = request.form.get('telefon', '').strip()

        if not ad or not soyad:
            flash('Ad ve Soyad zorunludur!')
            return redirect(url_for('add_personel'))

        if not telefon.isdigit() or len(telefon) != 11:
            flash('Telefon numarası 11 haneli olmalı ve sadece rakam içermelidir!')
            return redirect(url_for('add_personel'))

        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO personel (ad, soyad, departman, email, telefon)
                VALUES (?, ?, ?, ?, ?)
            ''', (ad, soyad, departman, email, telefon))
            conn.commit()
            flash('Personel başarıyla eklendi!')
        except sqlite3.IntegrityError:
            flash('Bu e-posta adresi zaten kullanılıyor!')
        finally:
            conn.close()

        return redirect(url_for('dashboard'))

    return render_template('add_personel.html')

# Personel Güncelleme Sayfası
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_personel(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    personel = conn.execute('SELECT * FROM personel WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        ad = request.form['ad'].strip()
        soyad = request.form['soyad'].strip()
        departman = request.form['departman'].strip()
        email = request.form['email'].strip()  # E-posta alanını ekle
        telefon = request.form['telefon'].strip()

        # Validasyon kontrolleri
        if not ad or not soyad or not email:
            flash('Ad, Soyad ve E-posta zorunludur!')
            conn.close()
            return redirect(url_for('update_personel', id=id))

        if not telefon.isdigit() or len(telefon) != 11:
            flash('Telefon numarası 11 haneli olmalı ve sadece rakam içermelidir!')
            conn.close()
            return redirect(url_for('update_personel', id=id))

        # E-posta format kontrolü
        import re
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, email):
            flash('Geçerli bir e-posta adresi giriniz!')
            conn.close()
            return redirect(url_for('update_personel', id=id))

        # E-posta benzersizlik kontrolü (kendisi hariç)
        existing_email = conn.execute('SELECT id FROM personel WHERE email = ? AND id != ?', (email, id)).fetchone()
        if existing_email:
            flash('Bu e-posta adresi başka bir personel tarafından kullanılıyor!')
            conn.close()
            return redirect(url_for('update_personel', id=id))

        try:
            # Tüm alanları güncelle (E-posta dahil)
            conn.execute('''UPDATE personel 
                           SET ad = ?, soyad = ?, departman = ?, email = ?, telefon = ? 
                           WHERE id = ?''', 
                        (ad, soyad, departman, email, telefon, id))
            conn.commit()
            flash('Personel başarıyla güncellendi!')
        except sqlite3.IntegrityError:
            flash('Bu e-posta adresi zaten kullanılıyor!')
        except Exception as e:
            flash(f'Güncelleme sırasında hata oluştu: {str(e)}')
        finally:
            conn.close()
        
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('update_personel.html', personel=personel)

# Personel Silme (Super Admin + Normal Admin)
@app.route('/delete/<int:id>')
def delete_personel(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Hem super admin hem normal admin silebilir (yetki kontrolü)
    conn = get_db_connection()
    conn.execute('DELETE FROM personel WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    idleri_sirala()  # ID'leri yeniden sırala
    flash('Personel başarıyla silindi!')
    return redirect(url_for('dashboard'))

def idleri_sirala():
    conn = get_db_connection()
    # Tüm sütunları kontrol et
    cursor = conn.execute("PRAGMA table_info(personel)")
    all_columns = [column[1] for column in cursor.fetchall()]
    
    # Personelleri al
    personeller = conn.execute('SELECT * FROM personel ORDER BY id').fetchall()
    
    # Tabloyu temizle
    conn.execute('DELETE FROM personel')
    conn.commit()
    
    # Yeniden ekle
    for i, p in enumerate(personeller, start=1):
        if 'profil_foto' in all_columns and 'son_giris_tarihi' in all_columns:
            conn.execute('''
                INSERT INTO personel (id, ad, soyad, departman, email, telefon, profil_foto, son_giris_tarihi, son_giris_saati)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (i, p['ad'], p['soyad'], p['departman'], p['email'], p['telefon'], 
                  p.get('profil_foto'), p.get('son_giris_tarihi'), p.get('son_giris_saati')))
        else:
            conn.execute('''
                INSERT INTO personel (id, ad, soyad, departman, email, telefon)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (i, p['ad'], p['soyad'], p['departman'], p['email'], p['telefon']))
    
    conn.commit()
    conn.close()

def kod_gonder(email, kod):
    msg = Message(
        subject='Giriş Kodunuz',
        recipients=[email],
        body=f"Giriş kodunuz: {kod}"
    )
    mail.send(msg)

@app.route('/personel_login', methods=['GET', 'POST'])
def personel_login():
    if request.method == 'POST':
        ad = request.form['ad'].strip()
        soyad = request.form['soyad'].strip()
        email = request.form['email'].strip()
        conn = get_db_connection()
        personel = conn.execute(
            'SELECT * FROM personel WHERE ad = ? AND soyad = ? AND email = ?',
            (ad, soyad, email)
        ).fetchone()
        if personel:
            # Kod üret ve mail gönder
            kod = str(random.randint(100000, 999999))
            session['giris_kodu'] = kod
            session['personel_email'] = email
            kod_gonder(email, kod)
            flash('Mail adresinize kod gönderildi.')
            conn.close()
            return redirect(url_for('personel_kod'))
        else:
            flash('Girilen bilgilerle kayıtlı personel bulunamadı!')
            conn.close()
    return render_template('personel_login.html')

@app.route('/personel_kod', methods=['GET', 'POST'])
def personel_kod():
    if request.method == 'POST':
        kod = request.form['kod']
        if kod == session.get('giris_kodu'):
            session['personel_giris'] = True
            return redirect(url_for('ise_giris'))
        else:
            flash('Kod yanlış!')
    return render_template('personel_kod.html')

@app.route('/ise_giris', methods=['GET', 'POST'])
def ise_giris():
    if not session.get('personel_giris'):
        return redirect(url_for('personel_login'))
    
    if request.method == 'POST':
        email = session.get('personel_email')
        tarih = datetime.now().strftime('%Y-%m-%d')
        saat = datetime.now().strftime('%H:%M:%S')
        
        conn = get_db_connection()
        # Personel bilgisini al
        personel = conn.execute('SELECT * FROM personel WHERE email = ?', (email,)).fetchone()
        
        if personel:
            # Yoklama tablosuna ekle
            conn.execute('INSERT INTO yoklama (email, tarih, saat) VALUES (?, ?, ?)', (email, tarih, saat))
            
            # Güvenli güncelleme - sütun var mı kontrol et
            try:
                conn.execute('UPDATE personel SET son_giris_tarihi = ?, son_giris_saati = ? WHERE email = ?', (tarih, saat, email))
            except sqlite3.OperationalError:
                print("son_giris sütunları bulunamadı, sadece yoklama kaydedildi.")
                
            conn.commit()
            
            # API'den motivasyonel söz al
            rastgele_soz = turkce_api_den_soz_al()
            
            # Session'a güvenli şekilde veri ekle (sqlite3.Row için)
            session['motivasyon_soz'] = rastgele_soz
            session['personel_ad'] = personel['ad'] if personel['ad'] else 'Personel'
            session['personel_soyad'] = personel['soyad'] if personel['soyad'] else ''
            
            # Profil foto kontrolü
            try:
                session['personel_profil_foto'] = personel['profil_foto'] if personel['profil_foto'] else None
            except (KeyError, IndexError):
                session['personel_profil_foto'] = None
                
            # Departman kontrolü
            try:
                session['personel_departman'] = personel['departman'] if personel['departman'] else 'Genel'
            except (KeyError, IndexError):
                session['personel_departman'] = 'Genel'
            
            conn.close()
            return redirect(url_for('motivasyon_sayfasi'))
        else:
            conn.close()
            flash('Personel bulunamadı!')
            return redirect(url_for('personel_login'))
    
    return render_template('ise_giris.html')

@app.route('/yoklama')
def yoklama():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    yoklamalar = conn.execute('SELECT * FROM yoklama ORDER BY tarih DESC, saat DESC').fetchall()
    conn.close()
    return render_template('yoklama.html', yoklamalar=yoklamalar)

@app.route('/yoklama_excel')
def yoklama_excel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    yoklamalar = conn.execute('SELECT * FROM yoklama ORDER BY tarih DESC, saat DESC').fetchall()
    conn.close()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['E-posta', 'Tarih', 'Saat'])
    for y in yoklamalar:
        cw.writerow([y['email'], y['tarih'], y['saat']])
    output = si.getvalue()
    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=yoklama.csv"})

@app.route('/gunluk_rapor_gonder')
def gunluk_rapor_gonder():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Rapor gönderimini kontrol et
    sonuc = gunluk_rapor_mail()
    
    if sonuc:
        flash('Günlük raporlar başarıyla gönderildi! 📧✅')
    else:
        flash('Rapor gönderiminde hata oluştu! ❌')
    
    return redirect(url_for('dashboard'))

def gunluk_rapor_mail():
    conn = get_db_connection()
    # Tüm adminlerin e-postalarını al
    admins = conn.execute('SELECT email FROM admin WHERE email IS NOT NULL AND email != ""').fetchall()
    
    # Bugünkü tarihi al
    bugun = datetime.now().strftime('%Y-%m-%d')
    
    # Bugünkü yoklamaları al
    yoklamalar = conn.execute('''
        SELECT y.email, y.tarih, y.saat, p.ad, p.soyad, p.departman 
        FROM yoklama y
        LEFT JOIN personel p ON y.email = p.email
        WHERE y.tarih = ?
        ORDER BY y.saat
    ''', (bugun,)).fetchall()
    
    # Toplam personel sayısı
    toplam_personel = conn.execute('SELECT COUNT(*) as total FROM personel').fetchone()
    conn.close()
    
    # Rapor içeriği hazırla
    rapor = f"""
📊 GÜNLÜK YOKLAMA RAPORU
📅 Tarih: {bugun}
⏰ Rapor Saati: {datetime.now().strftime('%H:%M:%S')}

📈 ÖZET BİLGİLER:
• Toplam Personel: {toplam_personel['total']}
• Bugün Gelen: {len(yoklamalar)}
• Gelmeyenler: {toplam_personel['total'] - len(yoklamalar)}
• Katılım Oranı: %{round((len(yoklamalar) / toplam_personel['total']) * 100, 1) if toplam_personel['total'] > 0 else 0}

{'='*50}

📋 BUGÜN GELEN PERSONELLER:
"""
    
    if yoklamalar:
        for y in yoklamalar:
            ad_soyad = f"{y['ad']} {y['soyad']}" if y['ad'] and y['soyad'] else "Bilinmeyen Personel"
            departman = y['departman'] if y['departman'] else "Belirtilmemiş"
            rapor += f"""
👤 {ad_soyad}
📧 {y['email']}
🏢 {departman}
⏰ Giriş Saati: {y['saat']}
"""
    else:
        rapor += "\n❌ Bugün hiçbir personel işe gelmedi.\n"
    
    # Gelmeyen personelleri bul
    rapor += f"\n{'='*50}\n\n❌ BUGÜN GELMEYENLERİ:"
    
    conn = get_db_connection()
    gelmeyenler = conn.execute('''
        SELECT p.ad, p.soyad, p.email, p.departman
        FROM personel p
        WHERE p.email NOT IN (
            SELECT y.email FROM yoklama y WHERE y.tarih = ?
        )
    ''', (bugun,)).fetchall()
    conn.close()
    
    if gelmeyenler:
        for g in gelmeyenler:
            ad_soyad = f"{g['ad']} {g['soyad']}"
            departman = g['departman'] if g['departman'] else "Belirtilmemiş"
            rapor += f"""
👤 {ad_soyad}
📧 {g['email']}
🏢 {departman}
"""
    else:
        rapor += "\n✅ Tüm personel bugün işe geldi! 🎉\n"
    
    rapor += f"""
{'='*50}

Bu rapor otomatik olarak sistem tarafından oluşturulmuştur.
🕐 Son güncelleme: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

İyi günler dileriz! 😊
"""
    
    # Admin e-postalarını hazırla
    admin_emails = [a['email'] for a in admins if a['email']]
    
    if not admin_emails:
        print("❌ Gönderilecek admin e-postası bulunamadı!")
        return False
    
    try:
        # Mail gönder
        msg = Message(
            subject=f'📊 Günlük Yoklama Raporu - {bugun}',
            recipients=admin_emails,
            body=rapor
        )
        mail.send(msg)
        print(f"✅ Rapor başarıyla gönderildi: {admin_emails}")
        return True
    except Exception as e:
        print(f"❌ Mail gönderme hatası: {e}")
        return False

@app.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    # Sadece super admin ekleyebilsin
    if not session.get('logged_in'):
        flash('Giriş yapmalısınız!')
        return redirect(url_for('login'))
    if not session.get('is_super_admin'):
        flash('Sadece super admin yeni admin ekleyebilir!')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO admin (username, password, email) VALUES (?, ?, ?)', (username, hashed_password, email))
            conn.commit()
            flash('Yeni admin başarıyla eklendi!', 'success')
        except sqlite3.IntegrityError:
            flash('Bu kullanıcı adı zaten mevcut!', 'danger')
        finally:
            conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_admin.html')

# Admin Silme (Sadece Super Admin)
@app.route('/delete_admin/<int:id>')
def delete_admin(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Sadece super admin silebilir
    if not session.get('is_super_admin'):
        flash('Sadece super admin diğer adminleri silebilir!')
        return redirect(url_for('dashboard'))
    
    # Kendi kendini silmeye çalışıyor mu?
    conn = get_db_connection()
    silinecek_admin = conn.execute('SELECT username FROM admin WHERE id = ?', (id,)).fetchone()
    
    if silinecek_admin and silinecek_admin['username'] == session.get('username'):
        flash('Kendi hesabınızı silemezsiniz!')
        conn.close()
        return redirect(url_for('dashboard'))
    
    # Admin sil
    conn.execute('DELETE FROM admin WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Admin başarıyla silindi!')
    return redirect(url_for('dashboard'))

# Motivasyon API fonksiyonları
@app.route('/api/motivasyon')
def api_motivasyon():
    motivasyon_sozleri = [
        "Başarı, küçük çabaların günde tekrarlanmasıdır! 💪",
        "Bugün harika işler yapacağınızı biliyorum! ✨",
        "Her yeni gün, yeni fırsatlar getirir! 🌟",
        "Motivasyonunuz sizi başlatır, alışkanlık sizi devam ettirir! 🚀",
        "Büyük işler yapmak için, yaptığınız işi sevmelisiniz! ❤️",
        "Başarılı olmak için önce başarılı olacağınıza inanmalısınız! 🎯",
        "Her gün daha iyi bir versiyonunuz olun! 📈",
        "İmkansız, sadece büyük bir kelimedir! 💎",
        "Hedefinize odaklanın, engeller sadece illüzyondur! 🎪",
        "Bugün mükemmel bir gün olmaya başlıyor! ☀️",
        "Çalışkanlık şansın annesidir! 🍀",
        "Hayallerinizi gerçekleştirmek için çalışın! 🌈",
        "Pozitif düşünceler, pozitif sonuçlar yaratır! 😊",
        "Bugün yapacağınız işler yarınınızı şekillendirir! 🔮",
        "Mükemmellik bir tesadüf değil, alışkanlıktır! ⭐"
    ]
    return random.choice(motivasyon_sozleri)

def turkce_api_den_soz_al():
    try:
        # Kendi API'mizi çağır
        response = requests.get('http://127.0.0.1:5000/api/motivasyon', timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return "Her gün yeni bir başlangıçtır! 🌅"
    except:
        return "Bugün mükemmel işler yapacaksınız! ⭐"

@app.route('/motivasyon')
def motivasyon_sayfasi():
    if not session.get('motivasyon_soz'):
        return redirect(url_for('index'))
    return render_template('motivasyon.html')

@app.route('/clear_motivation_session', methods=['POST'])
def clear_motivation_session():
    session.pop('motivasyon_soz', None)
    session.pop('personel_ad', None)
    session.pop('personel_soyad', None)
    session.pop('personel_profil_foto', None)
    session.pop('personel_departman', None)
    return '', 204

# Admin Profil Güncelleme
@app.route('/update_admin/<int:id>', methods=['GET', 'POST'])
def update_admin(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    admin = conn.execute('SELECT * FROM admin WHERE id = ?', (id,)).fetchone()
    
    # Kendi profilini güncelliyor mu, yoksa başkasının mı?
    if admin['username'] != session.get('username') and not session.get('is_super_admin'):
        flash('Sadece kendi profilinizi güncelleyebilirsiniz!')
        conn.close()
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        
        # Username değişikliği kontrolü
        if username != admin['username']:
            # Super admin değişikliği yapıyor mu?
            if not session.get('is_super_admin'):
                flash('Kullanıcı adını değiştirme yetkiniz yok!')
                conn.close()
                return redirect(url_for('update_admin', id=id))
            
            # Username zaten var mı?
            existing = conn.execute('SELECT id FROM admin WHERE username = ? AND id != ?', (username, id)).fetchone()
            if existing:
                flash('Bu kullanıcı adı zaten kullanılıyor!')
                conn.close()
                return redirect(url_for('update_admin', id=id))
        
        # Şifre güncellemesi
        if password:
            hashed_password = generate_password_hash(password)
            conn.execute('UPDATE admin SET username = ?, email = ?, password = ? WHERE id = ?', 
                        (username, email, hashed_password, id))
        else:
            # Şifre değiştirilmiyorsa
            conn.execute('UPDATE admin SET username = ?, email = ? WHERE id = ?', 
                        (username, email, id))
        
        conn.commit()
        conn.close()
        
        # Kendi profilini güncelliyorsa session'ı güncelle
        if admin['username'] == session.get('username'):
            session['username'] = username
            session['admin_email'] = email
        
        flash('Profil başarıyla güncellendi!')
        return redirect(url_for('dashboard'))
    
    conn.close()
    return render_template('update_admin.html', admin=admin)

# Debug için rapor önizleme (geliştirme aşamasında kullan)
@app.route('/rapor_preview')
def rapor_preview():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    bugun = datetime.now().strftime('%Y-%m-%d')
    bugun_tr = datetime.now().strftime('%d.%m.%Y')
    
    # Personel ID'si de dahil edilecek şekilde sorgu
    yoklamalar = conn.execute('''
        SELECT y.email, y.tarih, y.saat, p.id, p.ad, p.soyad, p.departman 
        FROM yoklama y
        LEFT JOIN personel p ON y.email = p.email
        WHERE y.tarih = ?
        ORDER BY y.saat
    ''', (bugun,)).fetchall()
    
    toplam_personel = conn.execute('SELECT COUNT(*) as total FROM personel').fetchone()
    
    # Gelmeyen personelleri bul (ID dahil)
    gelmeyenler = conn.execute('''
        SELECT p.id, p.ad, p.soyad, p.email, p.departman
        FROM personel p
        WHERE p.email NOT IN (
            SELECT y.email FROM yoklama y WHERE y.tarih = ?
        )
    ''', (bugun,)).fetchall()
    conn.close()
    
    katilim_orani = round((len(yoklamalar) / toplam_personel['total']) * 100, 1) if toplam_personel['total'] > 0 else 0
    
    # Modern HTML rapor sayfası
    html_rapor = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Rapor Önizleme</title>
        <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.ico') }}">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
        <style>
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding: 20px 0;
            }}
            
            .report-container {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                margin: 20px auto;
                max-width: 1000px;
                overflow: hidden;
                animation: slideIn 0.6s ease-out;
            }}
            
            @keyframes slideIn {{
                from {{ opacity: 0; transform: translateY(-30px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            .report-header {{
                background: linear-gradient(135deg, #28a745, #20c997);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            
            .report-title {{
                font-size: 2.5rem;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            
            .report-date {{
                font-size: 1.2rem;
                opacity: 0.9;
            }}
            
            .stats-row {{
                background: #f8f9fa;
                padding: 30px;
                border-bottom: 1px solid #e9ecef;
            }}
            
            .stat-card {{
                background: white;
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
                transition: transform 0.3s ease;
                height: 100%;
            }}
            
            .stat-card:hover {{
                transform: translateY(-5px);
            }}
            
            .stat-number {{
                font-size: 2.5rem;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            
            .stat-label {{
                color: #6c757d;
                font-size: 1rem;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .stat-success {{ color: #28a745; }}
            .stat-primary {{ color: #007bff; }}
            .stat-warning {{ color: #ffc107; }}
            .stat-info {{ color: #17a2b8; }}
            
            .content-section {{
                padding: 30px;
            }}
            
            .section-title {{
                font-size: 1.5rem;
                font-weight: 600;
                color: #495057;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #e9ecef;
            }}
            
            .personel-card {{
                background: #f8f9fa;
                border-left: 4px solid #28a745;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
                transition: all 0.3s ease;
            }}
            
            .personel-card:hover {{
                background: #e9ecef;
                transform: translateX(5px);
            }}
            
            .absent-card {{
                border-left-color: #dc3545;
                background: #fff5f5;
            }}
            
            .absent-card:hover {{
                background: #ffe6e6;
            }}
            
            .personel-name {{
                font-weight: 600;
                color: #212529;
                margin-bottom: 5px;
            }}
            
            .personel-info {{
                color: #6c757d;
                font-size: 0.9rem;
            }}
            
            .time-badge {{
                background: #e3f2fd;
                color: #1976d2;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 0.85rem;
                font-weight: 500;
            }}
            
            .dept-badge {{
                background: #f3e5f5;
                color: #7b1fa2;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 0.85rem;
                font-weight: 500;
            }}
            
            .back-btn {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                border-radius: 25px;
                padding: 12px 30px;
                font-weight: 600;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 8px;
                transition: all 0.3s ease;
                margin: 5px;
            }}
            
            .back-btn:hover {{
                background: linear-gradient(135deg, #5a6fd8, #6a42a0);
                color: white;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }}
            
            .btn-edit {{
                background: linear-gradient(135deg, #28a745, #20c997);
            }}
            
            .btn-edit:hover {{
                background: linear-gradient(135deg, #20c997, #17a2b8);
            }}
            
            .btn-delete {{
                background: linear-gradient(135deg, #dc3545, #e55564);
            }}
            
            .btn-delete:hover {{
                background: linear-gradient(135deg, #c82333, #d14251);
            }}
            
            .no-data {{
                text-align: center;
                color: #6c757d;
                font-style: italic;
                padding: 40px;
                background: #f8f9fa;
                border-radius: 10px;
                margin: 20px 0;
            }}
            
            .action-buttons {{
                display: flex;
                gap: 5px;
                margin-top: 10px;
            }}
            
            .btn-sm {{
                padding: 5px 10px;
                font-size: 0.8rem;
                border-radius: 15px;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="report-container">
                <!-- Header -->
                <div class="report-header">
                    <div class="report-title">
                        <i class="bi bi-bar-chart-line me-3"></i>
                        Günlük Yoklama Raporu
                    </div>
                    <div class="report-date">
                        <i class="bi bi-calendar3"></i> {bugun_tr}
                        <span class="ms-3">
                            <i class="bi bi-clock"></i> {datetime.now().strftime('%H:%M:%S')}
                        </span>
                    </div>
                </div>
                
                <!-- İstatistikler -->
                <div class="stats-row">
                    <div class="row g-4">
                        <div class="col-md-3">
                            <div class="stat-card">
                                <div class="stat-number stat-primary">{toplam_personel['total']}</div>
                                <div class="stat-label">
                                    <i class="bi bi-people"></i> Toplam Personel
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="stat-card">
                                <div class="stat-number stat-success">{len(yoklamalar)}</div>
                                <div class="stat-label">
                                    <i class="bi bi-check-circle"></i> Bugün Gelen
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="stat-card">
                                <div class="stat-number stat-warning">{len(gelmeyenler)}</div>
                                <div class="stat-label">
                                    <i class="bi bi-x-circle"></i> Gelmeyenler
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="stat-card">
                                <div class="stat-number stat-info">%{katilim_orani}</div>
                                <div class="stat-label">
                                    <i class="bi bi-graph-up"></i> Katılım Oranı
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="content-section">
                    <div class="row">
                        <!-- Gelen Personeller -->
                        <div class="col-lg-6">
                            <h3 class="section-title">
                                <i class="bi bi-check-circle-fill text-success"></i>
                                Bugün Gelen Personeller
                            </h3>
    """
    
    if yoklamalar:
        for y in yoklamalar:
            ad_soyad = f"{y['ad']} {y['soyad']}" if y['ad'] and y['soyad'] else "Bilinmeyen Personel"
            departman = y['departman'] if y['departman'] else "Belirtilmemiş"
            personel_id = y['id'] if y['id'] else "#"
            
            html_rapor += f"""
                            <div class="personel-card">
                                <div class="personel-name">
                                    <i class="bi bi-person-fill me-2"></i>{ad_soyad}
                                </div>
                                <div class="personel-info">
                                    <span class="dept-badge">{departman}</span>
                                    <span class="time-badge ms-2">{y['saat']}</span>
                                    <br><small class="text-muted mt-1 d-block">{y['email']}</small>
                                </div>
                                <div class="action-buttons">
                                    <a href="/update/{personel_id}" class="btn btn-sm back-btn btn-edit">
                                        <i class="bi bi-pencil"></i> Güncelle
                                    </a>
                                </div>
                            </div>
            """
    else:
        html_rapor += """
                            <div class="no-data">
                                <i class="bi bi-inbox" style="font-size: 3rem; color: #dee2e6;"></i>
                                <h5 class="mt-3">Bugün hiçbir personel işe gelmedi</h5>
                                <p>Henüz yoklama kaydı bulunmuyor.</p>
                            </div>
        """
    
    html_rapor += """
                        </div>
                        
                        <!-- Gelmeyenler -->
                        <div class="col-lg-6">
                            <h3 class="section-title">
                                <i class="bi bi-x-circle-fill text-danger"></i>
                                Bugün Gelmeyenler
                            </h3>
    """
    
    if gelmeyenler:
        for g in gelmeyenler:
            ad_soyad = f"{g['ad']} {g['soyad']}"
            departman = g['departman'] if g['departman'] else "Belirtilmemiş"
            
            html_rapor += f"""
                            <div class="personel-card absent-card">
                                <div class="personel-name">
                                    <i class="bi bi-person-dash me-2"></i>{ad_soyad}
                                </div>
                                <div class="personel-info">
                                    <span class="dept-badge">{departman}</span>
                                    <br><small class="text-muted mt-1 d-block">{g['email']}</small>
                                </div>
                                <div class="action-buttons">
                                    <a href="/update/{g['id']}" class="btn btn-sm back-btn btn-edit">
                                        <i class="bi bi-pencil"></i> Güncelle
                                    </a>
                                </div>
                            </div>
            """
    else:
        html_rapor += """
                            <div class="no-data">
                                <i class="bi bi-emoji-smile" style="font-size: 3rem; color: #28a745;"></i>
                                <h5 class="mt-3 text-success">Harika! 🎉</h5>
                                <p>Tüm personel bugün işe geldi!</p>
                            </div>
        """
    
    html_rapor += f"""
                        </div>
                    </div>
                    
                    <!-- Alt Bilgi ve Geri Dön -->
                    <div class="text-center mt-5 pt-4 border-top">
                        <p class="text-muted mb-3">
                            <i class="bi bi-info-circle"></i>
                            Bu rapor otomatik olarak sistem tarafından oluşturulmuştur.
                        </p>
                        <a href="/dashboard" class="back-btn">
                            <i class="bi bi-arrow-left"></i>
                            Yönetim Paneli'ne Dön
                        </a>
                        <a href="/gunluk_rapor_gonder" class="back-btn" 
                           onclick="return confirm('Raporu e-posta ile göndermek istediğinizden emin misiniz?')">
                            <i class="bi bi-envelope"></i>
                            Raporu Gönder
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    
    return html_rapor

if __name__ == '__main__':
    app.run(debug=True)
