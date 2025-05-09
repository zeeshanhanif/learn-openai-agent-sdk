from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Any
import json
import logging
from uuid import uuid4
from datetime import datetime
import os

from .models import Message
from .websocket_manager import ConnectionManager
from .agent import message_received
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize the app
app = FastAPI(
    title="Chatbot API",
    description="Simple chatbot API with WebSocket support and OpenAI integration",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
connections_messages: Dict[str, List[Message]] = {}

# WebSocket connection manager
manager = ConnectionManager()

# Initialize the chatbot agent
model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    logger.warning("OPENAI_API_KEY not found in environment variables. The agent will not work without an API key.")

# Welcome route
@app.get("/")
async def root():
    return {"message": "Welcome to the Chatbot API!"}

# Health check route
@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/chat")
async def test_chat():
    output, input_items = await message_received([{"content": "What is the capital of Pakistan?", "role": "user"}])
    return output

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Handle WebSocket connections for real-time chat.
    Each connection gets a unique ID and separate message history.
    """
    # Generate a unique connection ID
    connection_id = str(uuid4())
    
    # Accept the WebSocket connection
    await manager.connect(websocket, connection_id)
    logger.info(f"Client connected with ID: {connection_id}")
    
    # Initialize empty message history for this connection
    connections_messages[connection_id] = []
    
    try:
        # Send welcome message to the client
        # welcome_message = Message(
        #     content=chatbot.get_welcome_message(),
        #     sender="bot"
        # )
        # connections_messages[connection_id].append(welcome_message)
        
        # await manager.send_message(connection_id, welcome_message.model_dump())
        
        while True:
            # Receive JSON data from the WebSocket
            data = await websocket.receive_text()
            
            try:
                # Parse the JSON data
                message_data = json.loads(data)
                message_type = message_data.get("type", "")
                
                # Handle different message types
                if message_type == "message" or message_type == "chat_message":
                    # Get message content
                    content = message_data.get("content", message_data.get("message", ""))
                    
                    if not content:
                        await manager.send_error(connection_id, "Message content is required")
                        continue
                    
                    # Create the user message
                    user_message = Message(
                        content=content,
                        sender="user"
                    )
                    
                    # Store the message
                    connections_messages[connection_id].append(user_message)
                    
                   
                    
                    # # Get conversation history for context
                    # conversation_history = [
                    #     msg.model_dump() for msg in connections_messages[connection_id]
                    # ]
                    
                    # # Store the bot message
                    # connections_messages[connection_id].append(bot_message)
                    
                    # Send the bot response back to the client
                    await manager.send_message(connection_id, content)
                
                else:
                    # Unknown message type
                    await manager.send_error(connection_id, f"Unknown message type: {message_type}")
            
            except json.JSONDecodeError:
                # Invalid JSON
                await manager.send_error(connection_id, "Invalid JSON data")
    
    except WebSocketDisconnect:
        # Client disconnected
        manager.disconnect(connection_id)
        logger.info(f"Client {connection_id} disconnected")
        
        # Clean up message history
        connections_messages.pop(connection_id, None)
    
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"WebSocket error: {str(e)}")
        manager.disconnect(connection_id)
        
        # Clean up message history
        connections_messages.pop(connection_id, None) 