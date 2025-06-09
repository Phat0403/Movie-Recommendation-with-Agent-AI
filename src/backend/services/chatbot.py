from uuid import uuid4
import json

from core.chatbot import get_movie_recommendation
from db.redis_client import RedisClient

class ChatbotService:
    def __init__(self, redis_client: RedisClient = None):
        self.redis_client = redis_client 

    async def init_conversation(self):
        """
        Initialize a new conversation context.
        """
        conversation_id = str(uuid4())

        await self.redis_client.set(f"conversation:{conversation_id}",json.dumps({
            "history": []
        }),expire=3600)  # Set expiration to 1 hour
        return {
            "conversation_id": conversation_id,
            "messages": "Hi there! I'm here to help you with movie recommendations, answering questions, or anything else you need. What can I assist you with today: "
        }

    async def response_message(self, conversation_id: str, message: str):
        """
        Store a message in the conversation history.
        """
        
        conversation_history = await self.redis_client.get(f"conversation:{conversation_id}")
        if not conversation_history:
            raise ValueError("Conversation not found or has expired.")
        
        conversation_history = json.loads(conversation_history)["history"]
        response = get_movie_recommendation(message, history=conversation_history)
        history = response.get("history", conversation_history)
        history = {"history": history}
        await self.redis_client.set(f"conversation:{conversation_id}", json.dumps(history), expire=3600)  # Update history with expiration
        return {
            "conversation_id": conversation_id,
            "messages": response.get("message", ""),
            "tconsts": response.get("tconsts", []),
            "movie": response.get("movie", []), 
        }
        
async def main():
    from db.clients import get_redis_client
    redis_client = get_redis_client()
    chatbot_service = ChatbotService(redis_client)
    # session_id = "c038da01-b18e-4792-82f0-af3bfd6ec166"
    # conversation = await chatbot_service.init_conversation()
    # session_id = conversation.get("conversation_id")
    # conversation = await chatbot_service.response_message(session_id, "I want to watch a movie about space exploration")
    # print(f"Session ID: {session_id}")
    # print(f"Conversation: {conversation}")
    print(await redis_client.get("conversation:2f5e7f07-2e2f-4718-b5fc-416a31e2d5bd"))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())