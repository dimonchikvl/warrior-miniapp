from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "level": 1,
            "xp": 0,
            "strength": 0,
            "discipline": 0,
            "finance": 0,
            "content": 0
        }
    )
