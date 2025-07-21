import sqlite3

conn = sqlite3.connect('personel.db')
try:
    conn.execute('ALTER TABLE personel ADD COLUMN son_giris_tarihi TEXT')
except sqlite3.OperationalError:
    print("son_giris_tarihi zaten var")
try:
    conn.execute('ALTER TABLE personel ADD COLUMN son_giris_saati TEXT')
except sqlite3.OperationalError:
    print("son_giris_saati zaten var")
conn.commit()
conn.close()
print("Tablo güncellendi.")

from werkzeug.security import generate_password_hash
import sqlite3

conn = sqlite3.connect('personel.db')
conn.execute("DELETE FROM admin WHERE username = 'admin'")
conn.execute("INSERT INTO admin (username, password, email) VALUES (?, ?, ?)",
             ('admin', generate_password_hash('1234'), 'alperakpinar60@gmail.com'))
conn.commit()
conn.close()