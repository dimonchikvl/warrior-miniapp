import random

QUEST_POOL = [
    ("train", 40, "strength"),
    ("steps", 30, "discipline"),
    ("no_smoke", 50, "discipline"),
    ("video", 40, "content"),
    ("book", 20, "discipline"),
    ("meditate", 25, "discipline"),
]


def generate_daily_quests():
    return random.sample(QUEST_POOL, 3)


DAILY_QUESTS = generate_daily_quests()
