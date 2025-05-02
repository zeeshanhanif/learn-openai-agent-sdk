import chainlit as cl
from fastapi import FastAPI
import uvicorn
from .app import app

def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)
