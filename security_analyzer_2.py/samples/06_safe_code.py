import os
import sqlite3

def safe_database_query(username):
    # Güvenli kod: Parametreli sorgu kullanımı
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchall()

def safe_file_read(filename):
    # Güvenli kod: Dizin dışına çıkış engelleniyor
    base_dir = os.path.abspath("/var/www/uploads")
    target_path = os.path.abspath(os.path.join(base_dir, filename))
    
    if not target_path.startswith(base_dir):
        raise ValueError("Yetkisiz erişim denemesi!")
        
    with open(target_path, "r", encoding="utf-8") as f:
        return f.read()