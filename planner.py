# =========================
# 🧠 КБЖУ КАЛЬКУЛЯТОР (ПИТАНИЕ)
# =========================
def calc_kbju(weight, goal):
    """
    Расчёт КБЖУ под цель пользователя
    """

    # белок фиксированный (рост мышц/сохранение массы)
    protein = weight * 1.6

    # калории зависят от цели
    if goal == "bulk":
        calories = weight * 33   # профицит
    elif goal == "cut":
        calories = weight * 25   # дефицит
    else:
        calories = weight * 28   # баланс (исправлено)

    # жир всегда стабильный коэффициент
    fat = weight * 1

    # углеводы считаются остатком калорий
    carbs = (calories - protein * 4 - fat * 9) / 4

    return {
        "calories": int(calories),
        "protein": int(protein),
        "fat": int(fat),
        "carbs": int(carbs)
    }


# =========================
# 🚶 ШАГИ (ПРОГРЕССИЯ)
# =========================
def steps_plan(day):
    """
    Увеличение нагрузки по дням (НЕ streak)
    """

    base = 8000 + day * 300

    # ограничение, чтобы не было перегруза
    return min(base, 12000)


# =========================
# 💪 ТРЕНИРОВКИ
# =========================
def training(goal):
    """
    Простая генерация тренировочного плана
    """

    if goal == "bulk":
        return ["Грудь", "Спина", "Ноги"]

    if goal == "cut":
        return ["Full body", "Кардио 30-40 мин"]

    return ["Лёгкая активность / восстановление"]


# =========================
# 🔥 ГЕНЕРАЦИЯ ПЛАНА (ИСПРАВЛЕНО)
# =========================
def generate_plan(user):
    """
    Генерация персонального плана
    """

    # -------------------------
    # ⚠️ защита от битых данных
    # -------------------------
    if not user:
        return {"error": "user not found"}

    goal = user[2]
    weight = user[5]
    streak = user[12]

    # -------------------------
    # 🔥 CUT
    # -------------------------
    if goal == "cut":
        return {
            "type": "cut",
            "steps": steps_plan(streak),
            "kbju": calc_kbju(weight, "cut"),
            "training": training("cut")
        }

    # -------------------------
    # 💪 BULK
    # -------------------------
    if goal == "bulk":
        return {
            "type": "bulk",
            "steps": steps_plan(streak),
            "kbju": calc_kbju(weight, "bulk"),
            "training": training("bulk")
        }

    # -------------------------
    # 🧠 DISCIPLINE
    # -------------------------
    if goal == "discipline":
        return {
            "type": "discipline",
            "tasks": [
                "Не пропускать день",
                "Минимум 1 полезное действие"
            ]
        }

    # -------------------------
    # 📱 CONTENT
    # -------------------------
    if goal == "content":
        return {
            "type": "content",
            "tasks": [
                "Снять видео",
                "Смонтировать",
                "Выложить"
            ]
        }

    # -------------------------
    # 🧩 fallback
    # -------------------------
    return {
        "type": "default",
        "message": "Выбери цель"
    }
