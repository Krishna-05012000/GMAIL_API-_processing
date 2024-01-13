
import sqlite3

conn = sqlite3.connect('emails.db')
cursor = conn.cursor()

def create_tables():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY,
        message_id TEXT,
        from_address TEXT,
        to_address TEXT,
        subject TEXT,
        date_received DATETIME,
        body TEXT
    )
    ''')
    conn.commit()

def insert_email(message_id, from_address, to_address, subject, date_received, body):
    cursor.execute('''
    INSERT INTO emails (message_id, from_address, to_address, subject, date_received, body)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (message_id, from_address, to_address, subject, date_received, body))
    conn.commit()

create_tables()
