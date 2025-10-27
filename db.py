import sqlite3

DB_PATH = 'bank.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            pincode INTEGER NOT NULL,
            balance INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_user(username, pincode):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND pincode = ?', (username, pincode))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(username, pincode, balance=0):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, pincode, balance) VALUES (?, ?, ?)', (username, pincode, balance))
    conn.commit()
    conn.close()

def get_balance(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
    balance = cursor.fetchone()[0]
    conn.close()
    return balance

def update_balance(user_id, new_balance):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
    conn.commit()
    conn.close()