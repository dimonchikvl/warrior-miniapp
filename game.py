import time
from db import get_user, update_user

COOLDOWN = {}

# =========================
# ANTI-SPAM
# =========================
def can_click(uid):
    now = time.time()
    if uid in COOLDOWN and now - COOLDOWN[uid] < 1.5:
        return False
    COOLDOWN[uid] = now
    return True


# =========================
# XP SYSTEM
# =========================
def xp_needed(level):
    return 120 + (level - 1) * 80


TASKS = {
    "train": (40, "strength"),
    "steps": (30, "discipline"),
    "no_smoke": (50, "discipline"),
    "video": (40, "content"),
    "book": (20, "discipline")
}


# =========================
# 🧠 NUTRITION CALCULATOR (КБЖУ)
# =========================
def calc_kbju(weight, goal):
    protein = weight * 1.6

    if goal == "bulk":
        calories = weight * 33
    elif goal == "cut":
        calories = weight * 25
    else:
        calories = weight * 30

    fat = weight * 1
    carbs = (calories - protein * 4 - fat * 9) / 4

    return {
        "calories": int(calories),
        "protein": int(protein),
        "fat": int(fat),
        "carbs": int(carbs)
    }


# =========================
# 🚶 STEP PROGRESSION SYSTEM
# =========================
def steps_plan(day):
    base = 8000
    steps = base + day * 500
    return min(steps, 12000)


# =========================
# 💪 TRAINING PLAN
# =========================
def training_plan(goal):
    if goal == "bulk":
        return ["Грудь", "Спина", "Ноги", "Плечи"]

    if goal == "cut":
        return ["Full body", "Кардио 30-40 мин"]

    return ["Лёгкая активность / прогулка"]


# =========================
# 🧠 HABIT SYSTEM
# =========================
def habit_plan(habit):
    if habit == "smoking":
        return [
            "Уменьши на 1 сигарету",
            "Замени на воду",
            "10 глубоких вдохов"
        ]

    if habit == "gaming":
        return [
            "Играй только после задач",
            "Ограничь 1 час"
        ]

    if habit == "gambling":
        return [
            "Не заходи сегодня",
            "Замени на прогулку"
        ]

    return ["Фокус на контроль привычки"]


# =========================
# 🧩 MAIN XP LOGIC
# =========================
def add_xp(uid, amount, stat=None):
    user = get_user(uid)

    xp = user[1]
    level = user[2]
    coins = user[3]

    strength = user[4]
    discipline = user[5]
    finance = user[6]
    content = user[7]

    energy = user[8]

    if energy <= 0:
        return {"error": "нет энергии"}

    energy -= 8
    xp += amount
    coins += amount // 2

    if stat == "strength":
        strength += 1
    elif stat == "discipline":
        discipline += 1
    elif stat == "finance":
        finance += 1
    elif stat == "content":
        content += 1

    leveled_up = False

    while xp >= xp_needed(level):
        xp -= xp_needed(level)
        level += 1
        leveled_up = True

    update_user(uid, "xp", xp)
    update_user(uid, "level", level)
    update_user(uid, "coins", coins)

    update_user(uid, "strength", strength)
    update_user(uid, "discipline", discipline)
    update_user(uid, "finance", finance)
    update_user(uid, "content", content)

    update_user(uid, "energy", energy)

    return {
        "xp": xp,
        "level": level,
        "coins": coins,
        "strength": strength,
        "discipline": discipline,
        "finance": finance,
        "content": content,
        "energy": energy,
        "leveled_up": leveled_up
    }


# =========================
# 🔥 FULL AI PLAN GENERATOR
# =========================
def generate_plan(user):
    """
    user format (пример):
    {
        "goal": "cut",
        "weight": 80,
        "height": 180,
        "age": 20,
        "day": 3,
        "bad_habit": "smoking"
    }
    """

    goal = user["goal"]

    if goal == "cut":
        return {
            "type": "fat_loss",
            "steps": steps_plan(user["day"]),
            "kbju": calc_kbju(user["weight"], "cut"),
            "training": training_plan("cut")
        }

    if goal == "bulk":
        return {
            "type": "mass_gain",
            "steps": steps_plan(user["day"]),
            "kbju": calc_kbju(user["weight"], "bulk"),
            "training": training_plan("bulk")
        }

    if goal == "discipline":
        return {
            "type": "habit",
            "habit_plan": habit_plan(user["bad_habit"])
        }

    if goal == "content":
        return {
            "type": "creator",
            "content_plan": [
                "Идея видео",
                "Съёмка",
                "Монтаж",
                "Публикация"
            ]
        }
