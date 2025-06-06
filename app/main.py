from fastapi import FastAPI

from app.controllers import game_controller, user_controller

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(game_controller.router)
app.include_router(user_controller.router)
