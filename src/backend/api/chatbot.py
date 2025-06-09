from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse

from db.clients import get_redis_client
from services.chatbot import ChatbotService

def get_chatbot_service(redis_client=Depends(get_redis_client)) -> ChatbotService:
    return ChatbotService(redis_client=redis_client)

router = APIRouter()
@router.post("/init-conversation")
async def init_conversation(chatbot_service: ChatbotService = Depends(get_chatbot_service)):
    """
    Initialize a new conversation context.
    """
    try:
        conversation = await chatbot_service.init_conversation()
        return JSONResponse(content=conversation, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/response-message")
async def response_message(
    conversation_id: str = Body(..., embed=True, description="Conversation ID"),
    message: str = Body(..., embed=True, description="User message"),
    chatbot_service: ChatbotService = Depends(get_chatbot_service)
):
    """
    Store a message in the conversation history and get a response.
    """
    try:
        response = await chatbot_service.response_message(conversation_id, message)
        return JSONResponse(content=response, status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))