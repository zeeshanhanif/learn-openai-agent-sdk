from fastapi import FastAPI
from chainlit.utils import mount_chainlit
from pathlib import Path

app = FastAPI()


@app.get("/")
def read_main():
    return {"message": "Hello World from main app"}

mount_chainlit(app=app, target="src/demo_chainlit/chatbot.py", path="/chainlit")