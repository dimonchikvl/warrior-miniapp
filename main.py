from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from game import add_xp, TASKS
from db import get_user
from models import Task

app = FastAPI()


@app.post("/complete-task")
def complete_task(data: Task):

    if data.task not in TASKS:
        return JSONResponse({"error": "unknown task"})

    xp, stat = TASKS[data.task]

    add_xp(data.user_id, xp, stat)

    user = get_user(data.user_id)

    return user


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    (твой HTML как сейчас)
    """
