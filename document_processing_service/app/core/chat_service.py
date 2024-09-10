# app/core/chat_service.py
from app.core.vector_db_service import VectorDBService
import uuid

class ChatService:
    def __init__(self):
        self.chats = {}
        self.vector_db_service = VectorDBService()

    def create_chat_thread(self, asset_id: str):
        if not self.vector_db_service.asset_exists(asset_id):
            return None
        chat_thread_id = str(uuid.uuid4())
        self.chats[chat_thread_id] = {"asset_id": asset_id, "history": []}
        return chat_thread_id

    async def get_agent_response(self, chat_thread_id: str, user_message: str):
        if chat_thread_id not in self.chats:
            return "Chat thread not found"
        
        chat_data = self.chats[chat_thread_id]
        asset_id = chat_data["asset_id"]

        # Query the embedding for the asset
        embedding = self.vector_db_service.get_embedding(asset_id)
        
        # Call the RAG agent from LangChain here
        # Simulated RAG response (replace with real integration)
        agent_response = f"Response to '{user_message}' based on asset ID '{asset_id}'"

        # Store chat history
        chat_data["history"].append({"user": user_message, "agent": agent_response})
        return agent_response

    def get_chat_history(self, chat_thread_id: str):
        return self.chats.get(chat_thread_id, {}).get("history", [])
