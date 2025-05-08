from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
from pydantic import BaseModel
from .agent import message_received


# Configure logging
logger = logging.getLogger(__name__)

# class ConnectionInfo(BaseModel):
#     websocket: WebSocket
#     history: List[Any]

class ConnectionManager:
    """
    Simple WebSocket connection manager.
    Manages connections with unique connection IDs.
    """
    
    def __init__(self):
        """Initialize the connection manager."""
        # Map of connection_id to WebSocket connection
        self.active_connections: Dict[str, Dict[str, Any]] = {}
        self.connection_count = 0
    
    async def connect(self, websocket: WebSocket, connection_id: str) -> None:
        """
        Connect a new WebSocket client.
        
        Args:
            websocket: The WebSocket connection
            connection_id: Unique identifier for the connection
        """
        # Accept the connection
        await websocket.accept()
        
        # Store the connection
        # self.active_connections[connection_id] = websocket
        self.active_connections[connection_id] = {
            "websocket": websocket,
            "history": []
        }

        self.connection_count += 1

        logger.info(f"New connection: {connection_id}. Total connections: {self.connection_count}")
    
    def disconnect(self, connection_id: str) -> None:
        """
        Disconnect a WebSocket connection.
        
        Args:
            connection_id: ID of the connection to disconnect
        """
        if connection_id in self.active_connections:
            self.active_connections[connection_id]["websocket"].close()
            del self.active_connections[connection_id]
            self.connection_count -= 1
            # self.active_connections.pop(connection_id)
            logger.info(f"Connection removed: {connection_id}. Total connections: {len(self.active_connections)}")
    
    async def send_message(self, connection_id: str, message: Any) -> bool:
        """
        Send a message to a specific connection.
        
        Args:
            connection_id: The connection ID to send to
            message: The message object to send
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if connection_id not in self.active_connections:
            logger.warning(f"Cannot send message: connection {connection_id} not found")
            return False
            
        connection_info: Dict[str, Any] = self.active_connections[connection_id]
        try:
            message_history = connection_info["history"]
            message_history.append({"content": message, "role": "user"})
            final_output, input_items = await message_received(message_history)

            connection_info["history"] = input_items

            await connection_info["websocket"].send_json({
                "type": "message",
                "message": final_output
            })
            return True
        except WebSocketDisconnect:
            logger.warning(f"Client {connection_id} disconnected while sending message")
            self.disconnect(connection_id)
            return False
        except Exception as e:
            logger.error(f"Error sending message to {connection_id}: {str(e)}")
            self.disconnect(connection_id)
            return False
    
    async def send_chat_message(self, connection_id: str, content: str, sender: str) -> bool:
        """
        Send a chat message to a specific connection.
        
        Args:
            connection_id: The connection ID to send to
            content: The message content
            sender: The sender identifier (e.g., 'bot', 'system')
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if connection_id not in self.active_connections:
            logger.warning(f"Cannot send chat message: connection {connection_id} not found")
            return False
            
        websocket = self.active_connections[connection_id]["websocket"]
        try:
            await websocket.send_json({
                "type": "message",
                "message": {
                    "content": content,
                    "sender": sender,
                    "timestamp": datetime.now().isoformat()
                }
            })
            return True
        except WebSocketDisconnect:
            logger.warning(f"Client {connection_id} disconnected while sending chat message")
            self.disconnect(connection_id)
            return False
        except Exception as e:
            logger.error(f"Error sending chat message to {connection_id}: {str(e)}")
            self.disconnect(connection_id)
            return False
    
    async def send_error(self, connection_id: str, error_message: str) -> bool:
        """
        Send an error message to a specific connection.
        
        Args:
            connection_id: The connection ID to send to
            error_message: The error message
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if connection_id not in self.active_connections:
            logger.warning(f"Cannot send error: connection {connection_id} not found")
            return False
            
        connection_info: Dict[str, Any] = self.active_connections[connection_id]
        try:
            await connection_info["websocket"].send_json({
                "type": "error",
                "message": error_message
            })
            return True
        except WebSocketDisconnect:
            logger.warning(f"Client {connection_id} disconnected while sending error")
            self.disconnect(connection_id)
            return False
        except Exception as e:
            logger.error(f"Error sending error message to {connection_id}: {str(e)}")
            self.disconnect(connection_id)
            return False
    
    
    
    async def broadcast(self, message: Dict[str, Any], exclude: str = None) -> None:
        """
        Send a message to all connected clients except the excluded one.
        
        Args:
            message: The message to send
            exclude: Optional connection ID to exclude from broadcast
        """
        if not self.active_connections:
            return
        
        disconnected = []
        
        for conn_id, websocket in list(self.active_connections.items()):
            if exclude and conn_id == exclude:
                continue
                
            try:
                await websocket.send_json(message)
            except WebSocketDisconnect:
                disconnected.append(conn_id)
                logger.warning(f"Client {conn_id} disconnected during broadcast")
            except Exception as e:
                disconnected.append(conn_id)
                logger.error(f"Error broadcasting message to {conn_id}: {str(e)}")
        
        # Clean up disconnected clients
        for conn_id in disconnected:
            self.disconnect(conn_id) 