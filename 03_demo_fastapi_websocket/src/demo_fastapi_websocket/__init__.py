import uvicorn
from .app import app

def main() -> None:
    """Run the FastAPI application using uvicorn."""
    uvicorn.run("demo_fastapi_websocket.app:app", host="0.0.0.0", port=8000, reload=True)
    # uvicorn.run(app, host="0.0.0.0", port=8000)
