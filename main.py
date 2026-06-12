from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from game import add_xp, TASKS, can_click
from db import get_user, update_streak

app = FastAPI()


class Task(BaseModel):
    user_id: int
    task: str


@app.post("/complete-task")
def complete_task(data: Task):

    if not can_click(data.user_id):
        return {"error": "slow down"}

    if data.task not in TASKS:
        return {"error": "unknown task"}

    update_streak(data.user_id)

    xp, stat = TASKS[data.task]

    result = add_xp(data.user_id, xp, stat)

    user = get_user(data.user_id)

    return {
        **result,
        "streak": user[7]
    }


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Warrior RPG PRO</title>

<style>
body {
    background:#0f0f0f;
    color:white;
    font-family:Arial;
    text-align:center;
    padding:20px;
}

.card {
    background:#1c1c1c;
    padding:15px;
    margin:10px auto;
    width:320px;
    border-radius:12px;
}

button {
    width:320px;
    padding:12px;
    margin:6px;
    border-radius:10px;
    border:none;
    background:#2d6cdf;
    color:white;
    font-size:16px;
}

.bar {
    width:320px;
    height:10px;
    background:#333;
    border-radius:5px;
    margin:auto;
}

.fill {
    height:10px;
    background:#4caf50;
    width:0%;
}
</style>
</head>

<body>

<h1>⚔️ WARRIOR PRO</h1>

<div class="card">
<p id="level">Level: 1</p>
<p id="xp">XP: 0 / 100</p>
<div class="bar"><div id="bar" class="fill"></div></div>
<p id="streak">🔥 Streak: 0</p>
</div>

<div class="card">
<div>💪 <span id="str">0</span></div>
<div>🧠 <span id="disc">0</span></div>
<div>💰 <span id="fin">0</span></div>
<div>📱 <span id="cont">0</span></div>
</div>

<h3>Today quests</h3>

<button onclick="act('train')">🏋️ Train</button>
<button onclick="act('steps')">🚶 Steps</button>
<button onclick="act('no_smoke')">🚭 No smoke</button>
<button onclick="act('video')">🎥 Video</button>
<button onclick="act('book')">📚 Read</button>

<script>
async function act(task){

let uid = 1;

try {
 uid = window.Telegram.WebApp.initDataUnsafe.user.id;
}catch(e){}

const res = await fetch("/complete-task",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({user_id:uid,task:task})
});

const d = await res.json();

let need = 100 + (d.level-1)*60;
let percent = (d.xp/need)*100;

document.getElementById("level").innerText="Level: "+d.level;
document.getElementById("xp").innerText="XP: "+d.xp+" / "+need;
document.getElementById("bar").style.width=percent+"%";

document.getElementById("str").innerText=d.strength;
document.getElementById("disc").innerText=d.discipline;
document.getElementById("fin").innerText=d.finance;
document.getElementById("cont").innerText=d.content;

document.getElementById("streak").innerText="🔥 Streak: "+d.streak;

if(d.leveled_up){
alert("LEVEL UP ⚔️");
}
}
</script>

</body>
</html>
"""
