from fastapi import FastAPI

from app.controllers import game_controller

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(game_controller.router)
