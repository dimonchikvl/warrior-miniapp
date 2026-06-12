import sqlite3
from datetime import date
from typing import Optional, Dict, Any

conn = sqlite3.connect("game.db", check_same_thread=False)
conn.row_factory = sqlite3.Row  # 🔥 Возвращаем словари вместо кортежей
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
    
    strength INTEGER DEFAULT 0,
    discipline INTEGER DEFAULT 0,
    finance INTEGER DEFAULT 0,
    content INTEGER DEFAULT 0,
    
    streak INTEGER DEFAULT 0,
    last_day TEXT DEFAULT ''
)
""")

conn.commit()


# =========================
# 👤 GET USER (SAFE INIT FIXED)
# =========================
def get_user(uid: int) -> Optional[Dict[str, Any]]:
    """
    Получить пользователя по ID или создать нового
    Возвращает словарь для удобного доступа
    """
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
                strength,
                discipline,
                finance,
                content,
                streak,
                last_day
            )
            VALUES (?, 'onboarding', NULL, NULL, NULL, NULL, NULL, NULL,
                    0, 1, 0, 100, 0, 0, 0, 0, 0, '')
        """, (uid,))

        conn.commit()

        cur.execute("SELECT * FROM users WHERE user_id=?", (uid,))
        return cur.fetchone()

    return user


# =========================
# ✏️ UPDATE FIELD
# =========================
def update_user(uid: int, field: str, value: Any) -> None:
    """
    Обновить поле пользователя
    """
    cur.execute(f"UPDATE users SET {field}=? WHERE user_id=?", (value, uid))
    conn.commit()


# =========================
# 🔥 DAILY RESET (FIXED LOGIC V6)
# =========================
def reset_daily(uid: int) -> Dict[str, Any]:
    """
    Ежедневный сброс энергии и обновление серии
    Возвращает информацию о сбросе
    """
    user = get_user(uid)

    if not user:
        return {"error": "user not found"}

    today = str(date.today())

    last_day = user["last_day"] or ""
    streak = user["streak"] or 0

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
