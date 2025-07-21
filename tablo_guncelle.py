import sqlite3

def tablo_guncelle():
    conn = sqlite3.connect('personel.db')
    
    # Personel tablosuna eksik sütunları ekle
    try:
        conn.execute('ALTER TABLE personel ADD COLUMN son_giris_tarihi TEXT')
        print("son_giris_tarihi sütunu eklendi.")
    except sqlite3.OperationalError as e:
        print(f"son_giris_tarihi: {e}")
    
    try:
        conn.execute('ALTER TABLE personel ADD COLUMN son_giris_saati TEXT')
        print("son_giris_saati sütunu eklendi.")
    except sqlite3.OperationalError as e:
        print(f"son_giris_saati: {e}")
    
    try:
        conn.execute('ALTER TABLE personel ADD COLUMN profil_foto TEXT')
        print("profil_foto sütunu eklendi.")
    except sqlite3.OperationalError as e:
        print(f"profil_foto: {e}")
    
    conn.commit()
    conn.close()
    print("Veritabanı güncelleme tamamlandı!")

if __name__ == '__main__':
    tablo_guncelle()