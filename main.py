from fastapi import FastAPI
from routers import task,user

app = FastAPI()

app.include_router(task.router)
app.include_router(user.router)
