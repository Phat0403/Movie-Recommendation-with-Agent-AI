from uuid import uuid4
import json

from core.chatbot import chatbot_response
from db.redis_client import RedisClient
from db.es import ElasticSearchClient

class ChatbotService:
    def __init__(self, redis_client: RedisClient = None, es_client: ElasticSearchClient = None):
        self.redis_client = redis_client 
        self.es_client = es_client
        self.es_client.connect()

    async def init_conversation(self):
        """
        Initialize a new conversation context.
        """
        conversation_id = str(uuid4())
        return {
            "conversation_id": conversation_id,
            "messages": "Hi there! I'm here to help you with movie recommendations, answering questions, or anything else you need. What can I assist you with today: "
        }

    async def response_message(self, conversation_id: str, message: str):
        """
        Store a message in the conversation history.
        """
        
        response = await chatbot_response(
            user_query=message,
            es_client=self.es_client,
            session_id=conversation_id,
        )
        return {
            "conversation_id": conversation_id,
            "messages": response.get("message", ""),
            "tconsts": response.get("tconsts", []),
            "movie": response.get("movie", []), 
            "intent": response.get("intent", ""),
        }
        
async def main():
    from db.clients import get_redis_client, get_es_client
    redis_client = get_redis_client()
    es_client = get_es_client()
    chatbot_service = ChatbotService(redis_client, es_client)
    # session_id = "c038da01-b18e-4792-82f0-af3bfd6ec166"
    # conversation = await chatbot_service.init_conversation()
    # session_id = conversation.get("conversation_id")
    session_id = "b0479829-b755-4211-a6dd-a5a7275accef"
    conversation = await chatbot_service.response_message(session_id, "I want to choose the movie Spaceman")
    # print(f"Session ID: {session_id}")
    # print(f"Conversation: {conversation}")
    # print(await redis_client.get("conversation:2f5e7f07-2e2f-4718-b5fc-416a31e2d5bd"))
    print(conversation)
    await es_client.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())