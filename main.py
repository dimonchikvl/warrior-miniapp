from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from models import Task
from game import add_xp, TASKS, can_click
from db import get_user, reset_daily
from quests import DAILY_QUESTS
from shop import SHOP
from game import add_xp, TASKS, can_click
from db import get_user, reset_daily

app = FastAPI()


class Task(BaseModel):
    user_id: int
    task: str


@app.post("/complete-task")
def complete_task(data: Task):

    if not can_click(data.user_id):
        return {"error": "slow"}

    reset_daily(data.user_id)

    if data.task not in TASKS:
        return {"error": "unknown"}

    xp, stat = TASKS[data.task]

    result = add_xp(data.user_id, xp, stat)

    user = get_user(data.user_id)

    return {
        **result,
        "streak": user[9]
    }


# =========================
# MINI APP UI
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>WARRIOR V3</title>

<style>
body{
background:#0f0f0f;
color:white;
font-family:Arial;
text-align:center;
padding:20px;
}

.card{
background:#1c1c1c;
padding:15px;
margin:10px auto;
width:340px;
border-radius:12px;
}

button{
width:340px;
padding:12px;
margin:6px;
border-radius:10px;
border:none;
background:#2d6cdf;
color:white;
font-size:16px;
}

.shop{
background:#222;
padding:10px;
margin:5px;
border-radius:8px;
}
</style>
</head>

<body>

<h1>⚔️ WARRIOR V3</h1>

<div class="card">
<p id="level">Level 1</p>
<p id="xp">XP 0</p>
<p id="coins">Coins 0</p>
<p id="energy">Energy 100</p>
</div>

<div class="card">
<button onclick="act('train')">🏋️ Train</button>
<button onclick="act('steps')">🚶 Steps</button>
<button onclick="act('no_smoke')">🚭 No smoke</button>
<button onclick="act('video')">🎥 Video</button>
<button onclick="act('book')">📚 Book</button>
</div>

<div class="card">
<h3>🛒 Shop</h3>
<div class="shop">Energy +20 (100 coins)</div>
<div class="shop">XP Boost (150 coins)</div>
<div class="shop">Coin Boost (120 coins)</div>
</div>

<script>
async function act(task){

let uid = 1;

try{
 uid = window.Telegram.WebApp.initDataUnsafe.user.id;
}catch(e){}

const r = await fetch("/complete-task",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({user_id:uid,task:task})
});

const d = await r.json();

if(d.error){
alert(d.error);
return;
}

let need = 120 + (d.level-1)*80;

document.getElementById("level").innerText="Level "+d.level;
document.getElementById("xp").innerText="XP "+d.xp+" / "+need;
document.getElementById("coins").innerText="Coins "+d.coins;
document.getElementById("energy").innerText="Energy "+d.energy;

if(d.leveled_up){
alert("LEVEL UP ⚔️");
}
}
</script>

</body>
</html>
"""
