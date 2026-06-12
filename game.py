import time
from db import get_user, update_user

COOLDOWN = {}


def can_click(uid):
    now = time.time()
    if uid in COOLDOWN and now - COOLDOWN[uid] < 1.5:
        return False
    COOLDOWN[uid] = now
    return True


def xp_needed(level):
    return 120 + (level - 1) * 80


TASKS = {
    "train": (40, "strength"),
    "steps": (30, "discipline"),
    "no_smoke": (50, "discipline"),
    "video": (40, "content"),
    "book": (20, "discipline")
}


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
    # ===== NUTRITION SYSTEM =====
def calc_kbju(weight, goal):
    protein = weight * 1.6

    if goal == "bulk":
        calories = weight * 33
    elif goal == "cut":
        calories = weight * 25
    else:
        calories = weight * 30

    fat = weight * 1
    carbs = (calories - protein*4 - fat*9) / 4

    return {
        "calories": int(calories),
        "protein": int(protein),
        "fat": int(fat),
        "carbs": int(carbs)
    }
