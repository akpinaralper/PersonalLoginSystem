# filepath: c:\Users\Mavilly\Documents\personel_bilgi_sistemi\veritabani_olustur.py
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
def veritabani_olustur():
    conn = sqlite3.connect('personel.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS personel')

    cursor.execute('''
     CREATE TABLE personel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    soyad TEXT NOT NULL,
    departman TEXT,
    email TEXT UNIQUE,
    telefon TEXT
);
    ''')

    conn.commit()
    conn.close()
    print("Veritabanı başarıyla oluşturuldu!")

def yoklama_tablosu_olustur():
    conn = sqlite3.connect('personel.db')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS yoklama (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        tarih TEXT,
        saat TEXT
    )
    ''')
    conn.commit()
    conn.close()

def admin_tablosu_olustur():
    conn = sqlite3.connect('personel.db')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT
    )
    ''')
    conn.commit()
    conn.close()

def admin_verisi_ekle():
    conn = sqlite3.connect('personel.db')
    conn.execute("INSERT OR IGNORE INTO admin (username, password, email) VALUES (?, ?, ?)",
                 ('admin', '1234', 'alperakpinar60@gmail.com'))
    conn.commit()
    conn.close()
    
import sqlite3

conn = sqlite3.connect('personel.db')
try:
    conn.execute('ALTER TABLE personel ADD COLUMN son_giris_tarihi TEXT')
except sqlite3.OperationalError:
    pass  # Zaten varsa hata vermez
try:
    conn.execute('ALTER TABLE personel ADD COLUMN son_giris_saati TEXT')
except sqlite3.OperationalError:
    pass
conn.commit()
conn.close()

conn = sqlite3.connect('personel.db')
try:
    conn.execute('ALTER TABLE yoklama ADD COLUMN saat TEXT')
except sqlite3.OperationalError:
    pass
conn.commit()
conn.close()



if __name__ == '__main__':
    veritabani_olustur()
    yoklama_tablosu_olustur()
    admin_tablosu_olustur()
    admin_verisi_ekle()