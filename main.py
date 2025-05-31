from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Database
users_db = {}
tasks_db = {}

# Models
class User(BaseModel):
    id: str
    role: str  # 'parent' or 'child'
    name: str
    email: str

class Task(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str] = ""
    points: int
    required: bool
    type: str  # 'yesno', 'photo', 'mcq', 'ai', etc.
    days_active: List[str]

@app.get("/")
def read_root():
    return {"message": "DailySpark API is running."}

@app.post("/users", status_code=201)
def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.id] = user
    return user

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    if task.id in tasks_db:
        raise HTTPException(status_code=400, detail="Task already exists")
    tasks_db[task.id] = task
    return task

@app.get("/tasks/{user_id}", response_model=List[Task])
def get_tasks_for_user(user_id: str):
    return [task for task in tasks_db.values() if task.user_id == user_id]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
