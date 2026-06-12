from db import get_user, update_user


def xp_needed(level):
    return 100 + (level - 1) * 60


COOLDOWN = {}


def can_click(uid):
    import time
    now = time.time()

    if uid in COOLDOWN and now - COOLDOWN[uid] < 3:
        return False

    COOLDOWN[uid] = now
    return True


def add_xp(uid, amount, stat=None):
    user = get_user(uid)

    xp = user[1]
    level = user[2]

    strength = user[3]
    discipline = user[4]
    finance = user[5]
    content = user[6]

    xp += amount

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
    update_user(uid, "strength", strength)
    update_user(uid, "discipline", discipline)
    update_user(uid, "finance", finance)
    update_user(uid, "content", content)

    return {
        "xp": xp,
        "level": level,
        "strength": strength,
        "discipline": discipline,
        "finance": finance,
        "content": content,
        "leveled_up": leveled_up
    }


TASKS = {
    "train": (40, "strength"),
    "steps": (30, "discipline"),
    "no_smoke": (50, "discipline"),
    "video": (40, "content"),
    "book": (20, "discipline")
}
