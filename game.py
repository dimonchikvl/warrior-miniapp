import time
from typing import Optional, Dict, Any, Tuple
from db import get_user, update_user

# =========================
# ⛔ АНТИ-СПАМ (кулдаун кликов)
# =========================
COOLDOWN = {}

def can_click(uid: int) -> bool:
    """
    Запрещает спамить кнопки (1.5 сек задержка)
    """
    now = time.time()

    if uid in COOLDOWN and now - COOLDOWN[uid] < 1.5:
        return False

    COOLDOWN[uid] = now
    return True


# =========================
# 📊 ОПЫТ ДЛЯ УРОВНЕЙ
# =========================
def xp_needed(level: int) -> int:
    """
    Сколько XP нужно для следующего уровня
    """
    return 120 + (level - 1) * 80


# =========================
# 🎯 ЗАДАЧИ И НАГРАДЫ
# =========================
TASKS = {
    "train": (40, "strength"),
    "steps": (30, "discipline"),
    "no_smoke": (50, "discipline"),
    "video": (40, "content"),
    "book": (20, "discipline")
}


# =========================
# 🧠 КБЖУ КАЛЬКУЛЯТОР
# =========================
def calc_kbju(weight: int, goal: str) -> Dict[str, int]:
    """
    Расчёт калорий и БЖУ под цель
    """
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
# 🚶 ПРОГРЕСС ШАГОВ
# =========================
def steps_plan(day: int) -> int:
    """
    Увеличение шагов каждый день до 12000
    """
    base = 8000
    steps = base + day * 500
    return min(steps, 12000)


# =========================
# 💪 ТРЕНИРОВКИ
# =========================
def training_plan(goal: str) -> list:
    """
    План тренировок под цель
    """
    if goal == "bulk":
        return ["Грудь", "Спина", "Ноги", "Плечи"]

    if goal == "cut":
        return ["Full body", "Кардио 30-40 мин"]

    return ["Лёгкая активность / прогулка"]


# =========================
# 🧠 ПРИВЫЧКИ
# =========================
def habit_plan(habit: str) -> list:
    """
    План для отказа от привычек
    """
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
# 🧩 ОСНОВНАЯ XP ЛОГИКА
# =========================
def add_xp(uid: int, amount: int, stat: Optional[str] = None) -> Dict[str, Any]:
    """
    Добавляет XP, монеты и прокачку статов
    """

    user = get_user(uid)

    # защита от None
    if not user:
        return {"error": "user not found"}

    xp = user["xp"]
    level = user["level"]
    coins = user["coins"]

    strength = user["strength"]
    discipline = user["discipline"]
    finance = user["finance"]
    content = user["content"]

    energy = user["energy"]

    # если энергии нет — блок
    if energy <= 0:
        return {"error": "нет энергии"}

    # трата энергии
    energy -= 8

    # награды
    xp += amount
    coins += amount // 2

    # прокачка статов
    if stat == "strength":
        strength += 1
    elif stat == "discipline":
        discipline += 1
    elif stat == "finance":
        finance += 1
    elif stat == "content":
        content += 1

    leveled_up = False

    # проверка уровня
    while xp >= xp_needed(level):
        xp -= xp_needed(level)
        level += 1
        leveled_up = True

    # сохранение
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
# 🔥 ГЕНЕРАЦИЯ ПЛАНА (ИСПРАВЛЕНО)
# =========================
def generate_plan(user: Dict[str, Any]) -> Dict[str, Any]:
    """
    Генерация персонального плана
    """

    if not user:
        return {"error": "no user"}

    goal = user.get("goal")

    # защита от пустых значений
    weight = user.get("weight", 70)
    day = user.get("day", 1)
    bad_habit = user.get("bad_habit", "none")

    # =========================
    # 🔥 CUT
    # =========================
    if goal == "cut":
        return {
            "type": "cut",
            "steps": steps_plan(day),
            "kbju": calc_kbju(weight, "cut"),
            "training": training_plan("cut")
        }

    # =========================
    # 💪 BULK
    # =========================
    if goal == "bulk":
        return {
            "type": "bulk",
            "steps": steps_plan(day),
            "kbju": calc_kbju(weight, "bulk"),
            "training": training_plan("bulk")
        }

    # =========================
    # 🧠 DISCIPLINE
    # =========================
    if goal == "discipline":
        return {
            "type": "discipline",
            "habit": habit_plan(bad_habit)
        }

    # =========================
    # 📱 CONTENT
    # =========================
    if goal == "content":
        return {
            "type": "content",
            "tasks": [
                "Идея",
                "Съёмка",
                "Монтаж",
                "Публикация"
            ]
        }

    # fallback
    return {
        "type": "default",
        "message": "Выбери цель"
    }
