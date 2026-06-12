import sqlite3
from datetime import date

conn = sqlite3.connect("game.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,

    step TEXT DEFAULT 'onboarding',

    goal TEXT,
    age INTEGER,
    height INTEGER,
    weight INTEGER,
    activity TEXT,
    bad_habit TEXT,

    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    coins INTEGER DEFAULT 0,
    energy INTEGER DEFAULT 100,

    streak INTEGER DEFAULT 0,
    last_day TEXT DEFAULT ''
)
""")

conn.commit()


def get_user(uid):
    cur.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    user = cur.fetchone()

    if not user:
        cur.execute("INSERT INTO users(user_id) VALUES(?)", (uid,))
        conn.commit()
        return get_user(uid)

    return user


def update_user(uid, field, value):
    cur.execute(f"UPDATE users SET {field}=? WHERE user_id=?", (value, uid))
    conn.commit()


def reset_daily(uid):
    user = get_user(uid)
    today = str(date.today())

    if user[13] != today:
        update_user(uid, "energy", 100)
        update_user(uid, "last_day", today)
