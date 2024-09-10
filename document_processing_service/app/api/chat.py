# app/api/chat.py
from fastapi import APIRouter, HTTPException
from app.core.chat_service import ChatService
from fastapi.responses import StreamingResponse

router = APIRouter()
chat_service = ChatService()

@router.post("/api/chat/start")
async def start_chat(asset_id: str):
    chat_thread_id = chat_service.create_chat_thread(asset_id)
    if not chat_thread_id:
        raise HTTPException(status_code=400, detail="Invalid Asset ID")
    return {"chat_thread_id": chat_thread_id}

@router.post("/api/chat/message")
async def send_message(chat_thread_id: str, user_message: str):
    response = await chat_service.get_agent_response(chat_thread_id, user_message)
    return {"agent_response": response}

@router.get("/api/chat/history")
async def get_chat_history(chat_thread_id: str):
    history = chat_service.get_chat_history(chat_thread_id)
    return {"chat_history": history}
# app/api/chat.py (Add Streaming Response)

@router.post("/api/chat/message")
async def send_message_stream(chat_thread_id: str, user_message: str):
    async def message_stream():
        response = await chat_service.get_agent_response(chat_thread_id, user_message)
        for chunk in response.split():
            yield chunk + " "
            await asyncio.sleep(0.1)  # Simulating real-time stream delay
    return StreamingResponse(message_stream(), media_type="text/plain")

