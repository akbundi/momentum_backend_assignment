# chat_model.py

import uuid
from typing import Dict, List

class ChatThread:
    def __init__(self, asset_id: str):
        # Generate a unique chat thread ID
        self.thread_id = str(uuid.uuid4())
        self.asset_id = asset_id
        self.history: List[Dict[str, str]] = []
        
    def add_message(self, user_message: str, agent_response: str):
        """Store a message and the corresponding agent response in the chat history."""
        self.history.append({
            "user": user_message,
            "agent": agent_response
        })
    
    def get_history(self):
        """Retrieve the full chat history."""
        return self.history


class ChatModel:
    def __init__(self):
        # Maintain a dictionary of active chat threads
        self.threads: Dict[str, ChatThread] = {}
    
    def start_new_chat(self, asset_id: str) -> str:
        """Create a new chat thread associated with an asset ID."""
        new_thread = ChatThread(asset_id)
        self.threads[new_thread.thread_id] = new_thread
        return new_thread.thread_id
    
    def add_message_to_chat(self, thread_id: str, user_message: str, agent_response: str):
        """Add a message to the chat thread."""
        if thread_id in self.threads:
            self.threads[thread_id].add_message(user_message, agent_response)
        else:
            raise ValueError(f"Chat thread with ID {thread_id} not found")
    
    def get_chat_history(self, thread_id: str) -> List[Dict[str, str]]:
        """Get the full chat history of a thread."""
        if thread_id in self.threads:
            return self.threads[thread_id].get_history()
        else:
            raise ValueError(f"Chat thread with ID {thread_id} not found")
