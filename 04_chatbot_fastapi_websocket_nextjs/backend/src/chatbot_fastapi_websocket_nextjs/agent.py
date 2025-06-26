import os
import logging
from typing import Dict, List, Optional, Any, Tuple
from agents import Agent, Runner, TResponseInputItem
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

INSTRUCTIONS = """
You are a helpful, friendly assistant. Your job is to engage in conversation with users and provide helpful responses.
Be concise, respectful, and provide accurate information. If you don't know the answer to something, be honest about it.
Don't make up information or be overly verbose. Keep your responses focused and to the point.
"""

chat_agent = Agent(
    name="Chatbot Agent",
    model=model_name,
    instructions=INSTRUCTIONS,
)

async def message_received(messages: List[TResponseInputItem]) -> Tuple[Any, List[TResponseInputItem]]:
        """
        Process a message from the user.
        
        Args:
            message: The user's message
        """
        result = await Runner.run(chat_agent, messages)
        return result.final_output, result.to_input_list()