from pydantic import BaseModel

class Task(BaseModel):
    user_id: int
    task: str
