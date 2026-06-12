from db import get_user

def xp_needed(level):
    return 100 + (level - 1) * 50


def add_xp(uid, amount, stat=None):
    user = get_user(uid)

    user["xp"] += amount

    if stat:
        user[stat] += 1

    # level up
    while user["xp"] >= xp_needed(user["level"]):
        user["xp"] -= xp_needed(user["level"])
        user["level"] += 1


TASKS = {
    "train": (25, "strength"),
    "steps": (20, "discipline"),
    "no_smoke": (30, "discipline"),
    "video": (25, "content"),
    "book": (15, "discipline")
}
