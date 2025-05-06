from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import uuid4

def generate_id() -> str:
    """Generate a unique ID for an item."""
    return str(uuid4())

class ItemBase(BaseModel):
    """Base model for items."""
    name: str
    description: Optional[str] = None
    price: float = Field(ge=0.0)
    tags: list[str] = []
    metadata: Dict[str, Any] = {}

class ItemCreate(ItemBase):
    """Model for creating a new item."""
    pass

class ItemUpdate(BaseModel):
    """Model for updating an existing item."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0.0)
    tags: Optional[list[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class Item(ItemBase):
    """Model for an item with all fields."""
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        """Pydantic model configuration."""
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        } 