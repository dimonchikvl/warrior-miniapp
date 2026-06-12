from db import get_user, update_user


def xp_needed(level):
    return 100 + (level - 1) * 50


def add_xp(uid, amount, stat=None):
    user = get_user(uid)

    xp = user[1]
    level = user[2]

    strength = user[3]
    discipline = user[4]
    finance = user[5]
    content = user[6]

    # XP + stat
    xp += amount

    if stat == "strength":
        strength += 1
    elif stat == "discipline":
        discipline += 1
    elif stat == "finance":
        finance += 1
    elif stat == "content":
        content += 1

    # LEVEL UP
    while xp >= xp_needed(level):
        xp -= xp_needed(level)
        level += 1

    # SAVE
    update_user(uid, "xp", xp)
    update_user(uid, "level", level)
    update_user(uid, "strength", strength)
    update_user(uid, "discipline", discipline)
    update_user(uid, "finance", finance)
    update_user(uid, "content", content)
