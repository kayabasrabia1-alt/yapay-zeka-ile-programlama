import sqlite3

def get_user_data(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # Zafiyetli kod: Kullanıcı girdisi doğrudan sorgu dizisine ekleniyor
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()