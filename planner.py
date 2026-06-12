def calc_kbju(weight, goal):
    protein = weight * 1.6

    if goal == "bulk":
        calories = weight * 33
    else:
        calories = weight * 25

    fat = weight * 1
    carbs = (calories - protein*4 - fat*9) / 4

    return {
        "calories": int(calories),
        "protein": int(protein),
        "fat": int(fat),
        "carbs": int(carbs)
    }


def steps_plan(streak):
    base = 8000 + streak * 300
    return min(base, 12000)


def training(goal):
    if goal == "bulk":
        return ["Грудь", "Спина", "Ноги"]
    return ["Full body", "Кардио"]


def generate_plan(user):
    goal = user[2]
    weight = user[5]
    streak = user[12]

    if goal == "cut":
        return {
            "steps": steps_plan(streak),
            "kbju": calc_kbju(weight, "cut"),
            "training": training("cut")
        }

    if goal == "bulk":
        return {
            "steps": steps_plan(streak),
            "kbju": calc_kbju(weight, "bulk"),
            "training": training("bulk")
        }

    if goal == "discipline":
        return {
            "task": ["Не пропускать день", "Минимум 1 полезное действие"]
        }

    if goal == "content":
        return {
            "task": ["Снять", "Смонтировать", "Выложить"]
        }
