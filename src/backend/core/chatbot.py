from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_redis import RedisChatMessageHistory
from core.chatbot_prompt import QUERY_PROMPT_TEMPLATE, CHAT_PROMPT

from db.es import ElasticSearchClient
from db.clients import get_chroma_client, get_es_client
from config.config import Settings
from config.db_config import REDIS_URL

settings = Settings()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-05-20",
    temperature=0.5,
    max_output_tokens=1024,
    api_key=settings.GOOGLE_API_KEY
)
client = get_chroma_client()

def get_chat_history(session_id: str, redis_url: str = REDIS_URL) -> BaseChatMessageHistory:
    """
    Get chat history from Redis.
    
    Args:
        redis_url (str): The URL of the Redis server.
        session_id (str): The session ID to retrieve chat history for.
    
    Returns:
        BaseChatMessageHistory: The chat message history.
    """
    return RedisChatMessageHistory(session_id=session_id, 
                                   redis_url=redis_url,
                                   ttl=3600)  # Set TTL to 1 hour

def find_movie_recommendations(query: str, max_suggestions: int = 20) -> str:
    """
    Find movie recommendations based on user query.
    
    Args:
        query (str): The user query to search for movie recommendations.
        max_suggestions (int): Maximum number of movie suggestions to return.
    
    Returns:
        str: A string containing movie recommendations.
    """
    results = client.query(
        query_text=query,
        n_results=max_suggestions
    )
    documents = results.get('documents', [[]])[0]
    ids = results.get('ids', [[]])[0]
    texts = []
    for i in range(max_suggestions):
        text = documents[i]+"_"+str(ids[i])
        texts.append(text)

    texts = "\n".join(texts)
    return texts

async def find_movie_by_name(movie_name: str, es_client: ElasticSearchClient, max_suggestions: int = 10) -> str:
    """
    Fuzzy search movie titles in Elasticsearch index and return matched results.
    
    Args:
        movie_name (str): The name of the movie to search for.
        es_client (ElasticSearchClient): The Elasticsearch client instance.
        max_suggestions (int): Maximum number of movie suggestions to return.
    
    Returns:
        str: A string containing matched movie titles and IDs.
    """
    results = await es_client.fuzzy_search(
        index="movie",
        field="primaryTitle",
        value=movie_name,
        size=max_suggestions
    )
    documents = results.get('hits', {}).get('hits', [])
    texts = []
    for doc in documents:
        text = f"{doc['_source']['primaryTitle']}_{doc['_source']['description']}_{doc['_id']}"
        texts.append(text)
    
    return "\n".join(texts)

async def chatbot_response(user_query: str, es_client: ElasticSearchClient, max_suggestions: int = 15, session_id: str = "default_session"):
    """
    Retrieve movie recommendations based on user query and history.
    Uses ChromaDB to find relevant movies and LLM to generate recommendations.
    """
    history = get_chat_history(session_id)
    history_messages = history.messages
    for message in history_messages:
        print(f"History message: {message}")
    query_chain = QUERY_PROMPT_TEMPLATE | llm | JsonOutputParser()
    query_intent = query_chain.invoke({"query": user_query,
                                       "history": history},)
    query_type = query_intent.get("type", "chat")
    query_type = query_type.lower().strip()
    query_text = query_intent.get("query", "No information")
    print(f"Query type: {query_type}")
    print(f"Query text: {query_text}")
    chain = CHAT_PROMPT | llm 
    chat_chain_with_history = RunnableWithMessageHistory(
        chain,
        get_chat_history,
        input_variables=["query", "context"],
        history_messages_key="history"
    )
    chain_response = chat_chain_with_history | JsonOutputParser()
    if query_type == "search by movie name":
        movie_name = query_text.split(": ")[1] if ": " in query_text else query_text
        texts = await find_movie_by_name(movie_name, es_client, max_suggestions)
        if not texts:
            return {
                "message": "No movies found matching your query.",
                "tconsts": [],
                "movie": [],
                "intent": query_type
            }
        context = texts
    elif query_type == "search by description":
        context = find_movie_recommendations(query_text, max_suggestions)
    elif query_type == "choose a movie":
        context = "Choose the movie that the user is looking for from the list of movies in the history. Return the tconst as well as the movie name of the movie that the user is looking for."
    else:  # Normal chat
        context = "No specific context available, just respond to the user's query."

    response = chain_response.invoke(
        {"query": user_query,
         "context": context}, 
        config = {"configurable": {"session_id": session_id} }
    )

    return {
        "message": response.get("message", ""),
        "tconsts": response.get("tconsts", []),
        "movie": response.get("movie", []),
        "intent": query_type.lower().strip()
    }

async def main():
    es_client = get_es_client()
    es_client.connect()
    user_query = "I want to choose the movie Last Exit: Space"
    print(await chatbot_response(user_query, es_client, max_suggestions=10))
    await es_client.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())