# database/db.py

import sqlite3

def init_db():
    conn = sqlite3.connect("ai_interview.db", check_same_thread=False)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        password TEXT,
        role TEXT DEFAULT 'user'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        username TEXT,
        date TEXT,
        confidence INTEGER,
        filler_count INTEGER
    )
    """)

    conn.commit()

    return conn