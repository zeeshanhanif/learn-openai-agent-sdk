from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import pathlib
from typing import Dict, List, Optional, Any
import json
from datetime import datetime

from .models import Item, ItemCreate, ItemUpdate
from .websocket_manager import ConnectionManager

# Custom JSON encoder to handle datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

app = FastAPI(
    title="Demo FastAPI WebSocket New App",
    description="A simple FastAPI application with RESTful endpoints and WebSocket support",
    version="0.1.0"
)

# Get the directory where static files are located
static_dir = pathlib.Path(__file__).parent / "static"
print("static_dir = ",static_dir)
# Mount the static files directory
try:
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
except RuntimeError:
    # If the directory doesn't exist yet, create it
    static_dir.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# In-memory storage for demonstration purposes
items: Dict[str, Item] = {}
manager = ConnectionManager()

# Basic REST endpoints
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Render the main HTML page."""
    html_file = static_dir / "index.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text())
    else:
        return JSONResponse(content={"message": "Welcome to FastAPI WebSocket Demo! HTML UI is not available."})

@app.get("/info")
async def get_info():
    """Get API information."""
    return {"message": "Welcome to FastAPI WebSocket Demo!"}

@app.get("/items", response_model=List[Item])
async def get_items():
    return list(items.values())

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.post("/items", response_model=Item)
async def create_item(item: ItemCreate):
    # Create a new item with generated ID and timestamps
    new_item = Item(
        **item.model_dump(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    items[new_item.id] = new_item
    print("new_item = ",new_item)
    print()
    print("new_item.json = ",new_item.model_dump(mode='json'))
    
    # Notify all connected WebSocket clients
    # Use model_dump(mode='json') to handle datetime serialization automatically
    await manager.broadcast({"action": "create", "item": new_item.model_dump(mode='json')})
    
    return new_item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item_update: ItemUpdate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Get the existing item
    stored_item = items[item_id]
    
    # Update the item with the provided fields
    update_data = item_update.model_dump(exclude_unset=True)
    
    # Apply the updates to the stored item
    for field, value in update_data.items():
        setattr(stored_item, field, value)
    
    # Update the timestamp
    stored_item.updated_at = datetime.now()
    
    # Store the updated item
    items[item_id] = stored_item
    
    # Notify all connected WebSocket clients
    await manager.broadcast({"action": "update", "item": stored_item.model_dump(mode='json')})
    
    return stored_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    
    deleted_item = items.pop(item_id)
    
    # Notify all connected WebSocket clients
    await manager.broadcast({"action": "delete", "item_id": item_id})
    
    return JSONResponse(content={"message": f"Item {item_id} deleted"})

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        # Send initial data to the client
        await manager.send_personal_message({
            "action": "init", 
            "items": [item.model_dump(mode='json') for item in items.values()]
        }, websocket)
        
        # Listen for messages from the client
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                # Echo the message back to the client
                await manager.send_personal_message(
                    {"action": "echo", "message": message}, 
                    websocket
                )
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    {"error": "Invalid JSON format"}, 
                    websocket
                )
    
    except WebSocketDisconnect:
        manager.disconnect(websocket) 