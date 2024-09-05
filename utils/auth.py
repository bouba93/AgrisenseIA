import sqlite3

def get_db_connection():
    conn = sqlite3.connect('data/users.db')
    return conn

def check_login(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def add_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()
