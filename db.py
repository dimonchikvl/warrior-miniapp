import sqlite3
from datetime import date

conn = sqlite3.connect("game.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,

    strength INTEGER DEFAULT 0,
    discipline INTEGER DEFAULT 0,
    finance INTEGER DEFAULT 0,
    content INTEGER DEFAULT 0,

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


# DAILY STREAK LOGIC
def update_streak(uid):
    user = get_user(uid)
    today = str(date.today())

    last_day = user[8]
    streak = user[7]

    if last_day != today:
        if last_day == str(date.fromordinal(date.today().toordinal() - 1)):
            streak += 1
        else:
            streak = 1

        update_user(uid, "streak", streak)
        update_user(uid, "last_day", today)
