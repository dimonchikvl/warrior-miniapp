import sqlite3
from datetime import date

conn = sqlite3.connect("game.db", check_same_thread=False)
cur = conn.cursor()

# =========================
# 🧠 DATABASE
# =========================
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


# =========================
# 👤 GET USER (SAFE INIT FIXED)
# =========================
def get_user(uid):
    cur.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    user = cur.fetchone()

    # 🔥 если юзера нет — создаём полностью с дефолтами
    if not user:
        cur.execute("""
            INSERT INTO users(
                user_id,
                step,
                goal,
                age,
                height,
                weight,
                activity,
                bad_habit,
                xp,
                level,
                coins,
                energy,
                streak,
                last_day
            )
            VALUES (?, 'onboarding', NULL, NULL, NULL, NULL, NULL, NULL,
                    0, 1, 0, 100, 0, '')
        """, (uid,))

        conn.commit()

        cur.execute("SELECT * FROM users WHERE user_id=?", (uid,))
        return cur.fetchone()

    return user


# =========================
# ✏️ UPDATE FIELD
# =========================
def update_user(uid, field, value):
    cur.execute(f"UPDATE users SET {field}=? WHERE user_id=?", (value, uid))
    conn.commit()


# =========================
# 🔥 DAILY RESET (FIXED LOGIC V6)
# =========================
def reset_daily(uid):
    user = get_user(uid)

    today = str(date.today())

    last_day = user[13] or ""
    streak = user[12] or 0

    # =========================
    # 🧠 уже обновляли сегодня
    # =========================
    if last_day == today:
        return {
            "reset": False,
            "streak": streak
        }

    # =========================
    # 🔥 логика серии
    # =========================
    if last_day == "":
        new_streak = 1
    else:
        new_streak = streak + 1

    # =========================
    # 🔄 сброс дневных параметров
    # =========================
    update_user(uid, "energy", 100)
    update_user(uid, "streak", new_streak)
    update_user(uid, "last_day", today)

    return {
        "reset": True,
        "streak": new_streak
    }
