from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import uuid4


class Message(BaseModel):
    """Chat message model"""
    content: str
    sender: str
    timestamp: datetime = Field(default_factory=datetime.now)
    id: str = Field(default_factory=lambda: str(uuid4()))
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "content": "Hello, world!",
                "sender": "user",
                "timestamp": "2023-01-01T00:00:00Z",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            }
        }
    ) 