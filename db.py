users = {}

def get_user(uid):
    if uid not in users:
        users[uid] = {
            "xp": 0,
            "level": 1,
            "strength": 0,
            "discipline": 0,
            "finance": 0,
            "content": 0
        }
    return users[uid]
