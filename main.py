from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pydantic import BaseModel
from db import get_user
from game import add_xp

app = FastAPI()

# =========================
# TASK REWARDS
# =========================
TASKS = {
    "train": (25, "strength"),
    "steps": (20, "discipline"),
    "no_smoke": (30, "discipline"),
    "video": (25, "content"),
    "book": (15, "discipline")
}

# =========================
# MODEL
# =========================
class Task(BaseModel):
    user_id: int
    task: str

# =========================
# API: COMPLETE TASK
# =========================
@app.post("/complete-task")
def complete_task(data: Task):

    if data.task not in TASKS:
        return {"error": "unknown task"}

    xp, stat = TASKS[data.task]

    add_xp(data.user_id, xp, stat)

    user = get_user(data.user_id)

    return {
        "xp": user[1],
        "level": user[2],
        "strength": user[3],
        "discipline": user[4],
        "finance": user[5],
        "content": user[6],
        "streak": user[7]
    }

# =========================
# MINI APP FRONTEND
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Warrior RPG</title>

    <style>
        body {
            background: #0f0f0f;
            color: white;
            font-family: Arial;
            text-align: center;
            padding: 20px;
        }

        .card {
            background: #1c1c1c;
            padding: 15px;
            margin: 10px auto;
            width: 320px;
            border-radius: 12px;
        }

        button {
            width: 320px;
            padding: 12px;
            margin: 6px;
            border-radius: 10px;
            border: none;
            background: #2d6cdf;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        button:active {
            transform: scale(0.97);
        }

        .stats {
            display: flex;
            justify-content: space-around;
            margin-top: 10px;
        }
    </style>
</head>
<body>

<h1>⚔️ WARRIOR RPG</h1>

<div class="card">
    <p id="level">Уровень: 1</p>
    <p id="xp">XP: 0</p>
</div>

<div class="stats">
    <div>💪 <span id="strength">0</span></div>
    <div>🧠 <span id="discipline">0</span></div>
    <div>💰 <span id="finance">0</span></div>
    <div>📱 <span id="content">0</span></div>
</div>

<h3>Сегодня</h3>

<button onclick="complete('train')">🏋️ Тренировка</button>
<button onclick="complete('steps')">🚶 10000 шагов</button>
<button onclick="complete('no_smoke')">🚭 Без сигарет</button>
<button onclick="complete('video')">🎥 Выложить ролик</button>
<button onclick="complete('book')">📚 Прочитать 10 страниц</button>

<script>
async function complete(task) {

    let user_id = 1;

    try {
        user_id = window.Telegram.WebApp.initDataUnsafe.user.id;
    } catch (e) {}

    const res = await fetch("/complete-task", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: user_id,
            task: task
        })
    });

    const data = await res.json();

    document.getElementById("level").innerText =
        "Уровень: " + data.level;

    document.getElementById("xp").innerText =
        "XP: " + data.xp;

    document.getElementById("strength").innerText =
        data.strength;

    document.getElementById("discipline").innerText =
        data.discipline;

    document.getElementById("finance").innerText =
        data.finance;

    document.getElementById("content").innerText =
        data.content;
}
</script>

</body>
</html>
"""
