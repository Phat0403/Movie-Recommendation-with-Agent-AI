from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_redis import RedisChatMessageHistory
from core.chatbot_prompt import QUERY_PROMPT_TEMPLATE, CHAT_PROMPT, MOVIE_CONTENT_TEMPLATE

from db.es import ElasticSearchClient
from db.clients import get_chroma_client, get_es_client
from config.config import Settings
from config.db_config import REDIS_URL

settings = Settings()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
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

def get_recent_context(history_messages, limit: int = 2) -> str:
    """
    Extract the most recent conversation messages for context.
    
    Args:
        history_messages: List of chat messages
        limit: Number of recent messages to extract
    
    Returns:
        str: Formatted recent conversation context
    """
    if not history_messages:
        return "Không có lịch sử hội thoại."
    
    recent_messages = history_messages[-limit:] if len(history_messages) >= limit else history_messages
    context_parts = []
    
    for message in recent_messages:
        if hasattr(message, 'type'):
            role = "Người dùng" if message.type == "human" else "Bot"
            content = message.content if hasattr(message, 'content') else str(message)
            context_parts.append(f"{role}: {content}")
    
    return "\n".join(context_parts)

async def get_movie_content_from_llm(movie_name: str, user_query: str) -> str:
    """
    Use LLM knowledge to provide movie content information when database doesn't have it.
    
    Args:
        movie_name: Name of the movie
        user_query: User's specific question about the movie
    
    Returns:
        str: LLM-generated movie information
    """
    knowledge_prompt = f"""
    Bạn là một chuyên gia điện ảnh. Người dùng hỏi về phim "{movie_name}".
    Câu hỏi cụ thể: {user_query}
    
    Hãy cung cấp thông tin chi tiết về phim này dựa trên kiến thức của bạn, bao gồm:
    - Nội dung/cfabula chính
    - Diễn viên chính
    - Đạo diễn
    - Năm phát hành
    - Thể loại
    - Đánh giá/nhận xét
    
    Nếu không biết chắc chắn, hãy nói rõ và đưa ra thông tin có thể.
    Trả lời bằng tiếng Việt một cách tự nhiên và thân thiện.
    """
    
    try:
        response = llm.invoke(knowledge_prompt)
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        return f"Xin lỗi, tôi không thể tìm thấy thông tin về phim '{movie_name}' lúc này."

async def chatbot_response(user_query: str, es_client: ElasticSearchClient, max_suggestions: int = 15, session_id: str = "default_session"):
    """
    Retrieve movie recommendations based on user query and history.
    Uses ChromaDB to find relevant movies and LLM to generate recommendations.
    Enhanced with better context management and LLM fallback.
    """
    history = get_chat_history(session_id)
    history_messages = history.messages
    
    # Get recent context (last 2 messages) 
    recent_context = get_recent_context(history_messages, limit=2)
    print(f"History messages count: {len(history_messages)}")
    print(f"Recent context: {recent_context}")
    
    for message in history_messages:
        print(f"History message: {message}")
    
    # Enhanced query with recent context
    query_chain = QUERY_PROMPT_TEMPLATE | llm | JsonOutputParser()
    query_intent = query_chain.invoke({
        "query": user_query,
        "history": recent_context,  # Use recent context instead of full history
        "recent_conversation": recent_context  # Additional context for better understanding
    })
    
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
    
    # Enhanced context handling with LLM fallback
    if query_type == "search by movie name":
        movie_name = query_text.split(": ")[1] if ": " in query_text else query_text
        try:
            texts = await find_movie_by_name(movie_name, es_client, max_suggestions)
        except Exception as e:
            print(f"Elasticsearch error: {e}")
            texts = ""
        
        if not texts:
            # LLM Fallback: Use LLM knowledge when database doesn't have the movie
            llm_content = await get_movie_content_from_llm(movie_name, user_query)
            context = f"Thông tin từ kiến thức chung về phim '{movie_name}':\n{llm_content}"
        else:
            context = texts
            
    elif query_type == "search by description":
        context = find_movie_recommendations(query_text, max_suggestions)
        
    elif query_type == "choose a movie":
        context = f"Ngữ cảnh hội thoại gần đây:\n{recent_context}\n\nHãy chọn phim mà người dùng đang tìm kiếm từ danh sách phim trong lịch sử hội thoại. Trả về tconst cũng như tên phim mà người dùng đang tìm kiếm."
        
    elif "content" in query_type.lower() or "movie content" in query_type.lower() or is_movie_content_query(user_query, recent_context):
        # New intent: Ask about movie content - use specialized handler
        movie_name_from_context = extract_movie_name_from_context(recent_context, user_query)
        
        if movie_name_from_context:
            try:
                # Use specialized movie content handler
                content_response = await handle_movie_content_query(
                    movie_name_from_context, user_query, recent_context, es_client
                )
                # Also save to history manually for content queries
                history.add_user_message(user_query)
                history.add_ai_message(content_response.get("message", ""))
                return content_response
            except Exception as e:
                print(f"Error in movie content handler: {e}")
                # Fallback to LLM knowledge
                llm_content = await get_movie_content_from_llm(movie_name_from_context, user_query)
                context = f"Thông tin về phim '{movie_name_from_context}' từ kiến thức chung:\n{llm_content}"
        else:
            context = f"Ngữ cảnh hội thoại gần đây:\n{recent_context}\n\nHãy trả lời về nội dung phim dựa trên ngữ cảnh hoặc sử dụng kiến thức chung."
            
    else:  # Normal chat
        context = f"Ngữ cảnh hội thoại gần đây:\n{recent_context}\n\nTrả lời câu hỏi của người dùng một cách tự nhiên."

    response = chain_response.invoke(
        {"query": user_query,
         "context": context,
         "recent_context": recent_context}, 
        config = {"configurable": {"session_id": session_id} }
    )

    # Manually add messages to history after processing
    try:
        history.add_user_message(user_query)
        history.add_ai_message(response.get("message", ""))
        print(f"Added messages to history. New count: {len(history.messages)}")
    except Exception as e:
        print(f"Error saving to history: {e}")

    return {
        "message": response.get("message", ""),
        "tconsts": response.get("tconsts", []),
        "movie": response.get("movie", []),
        "intent": query_type.lower().strip(),
        "context_used": context[:200] + "..." if len(context) > 200 else context  # Debug info
    }

def extract_movie_name_from_context(recent_context: str, user_query: str) -> str:
    """
    Extract movie name from recent conversation context or current query.
    Enhanced for Vietnamese language and better context understanding.
    
    Args:
        recent_context: Recent conversation messages
        user_query: Current user query
    
    Returns:
        str: Extracted movie name or empty string
    """
    import re
    
    # Enhanced patterns for Vietnamese movie queries
    movie_patterns = [
        # Direct movie name mentions with quotes
        r'phim\s*["\'""„]([^"\'""„]+)["\'""„]',
        r'["\'""„]([^"\'""„]+)["\'""„]\s*(?:này|đó|kia)?',
        
        # Movie name after "phim" keyword
        r'phim\s+([A-Z][A-Za-z0-9\s\-:]+?)(?:\s|$|,|\.|;|\?|!)',
        r'về\s+phim\s+([A-Z][A-Za-z0-9\s\-:]+?)(?:\s|$|,|\.|;|\?|!)',
        
        # Movie name in context
        r'tên\s+phim\s+(?:là\s+)?([A-Z][A-Za-z0-9\s\-:]+?)(?:\s|$|,|\.|;|\?|!)',
        r'bộ\s+phim\s+([A-Z][A-Za-z0-9\s\-:]+?)(?:\s|$|,|\.|;|\?|!)',
        
        # Content-related queries
        r'nội\s+dung\s+(?:của\s+)?(?:phim\s+)?([A-Z][A-Za-z0-9\s\-:]+?)(?:\s|$|,|\.|;|\?|!)',
        r'cốt\s+truyện\s+(?:của\s+)?(?:phim\s+)?([A-Z][A-Za-z0-9\s\-:]+?)(?:\s|$|,|\.|;|\?|!)',
        
        # Last mentioned movie in context (look for capitalized words)
        r'([A-Z][A-Za-z0-9\s\-:]{2,30}?)(?:\s+có\s+nội\s+dung|như\s+thế\s+nào|\s+này)',
    ]
    
    combined_text = recent_context + " " + user_query
    
    # Try each pattern
    for pattern in movie_patterns:
        matches = re.findall(pattern, combined_text, re.IGNORECASE | re.MULTILINE)
        if matches:
            # Clean and validate the match
            movie_name = matches[0].strip()
            # Remove common suffixes and prefixes
            movie_name = re.sub(r'\s+(này|đó|kia|thì|à|nhỉ|không|chưa)$', '', movie_name, flags=re.IGNORECASE)
            movie_name = re.sub(r'^(phim|bộ|tập)\s+', '', movie_name, flags=re.IGNORECASE)
            
            # Validate length (movie names are usually between 2-50 characters)
            if 2 <= len(movie_name) <= 50 and not movie_name.lower() in ['nào', 'gì', 'đấy', 'này', 'kia']:
                return movie_name.strip()
    
    # Fallback: Look for any capitalized sequence that might be a movie name
    capitalized_sequences = re.findall(r'\b[A-Z][A-Za-z0-9\s\-:]{2,25}\b', combined_text)
    for seq in capitalized_sequences:
        seq = seq.strip()
        # Skip common Vietnamese words that get capitalized
        if seq.lower() not in ['bot', 'người dùng', 'gemini', 'ai', 'vietnamese', 'english']:
            return seq
    
    return ""

def is_movie_content_query(user_query: str, recent_context: str) -> bool:
    """
    Determine if the user is asking about movie content/details.
    
    Args:
        user_query: Current user query
        recent_context: Recent conversation context
    
    Returns:
        bool: True if asking about movie content
    """
    content_keywords = [
        'nội dung', 'cốt truyện', 'kể về', 'về cái gì', 'diễn viên', 'đạo diễn',
        'có biết', 'biết không', 'thể loại', 'ra mắt', 'năm nào', 'như thế nào',
        'content', 'plot', 'story', 'about what', 'actor', 'director'
    ]
    
    combined_text = (user_query + " " + recent_context).lower()
    
    return any(keyword in combined_text for keyword in content_keywords)

async def handle_movie_content_query(movie_name: str, user_query: str, recent_context: str, es_client: ElasticSearchClient) -> dict:
    """
    Handle movie content queries with enhanced context and LLM fallback.
    
    Args:
        movie_name: Name of the movie
        user_query: User's specific question
        recent_context: Recent conversation context
        es_client: Elasticsearch client
    
    Returns:
        dict: Formatted response with movie content information
    """
    # First try to get info from database
    database_info = ""
    try:
        movie_data = await find_movie_by_name(movie_name, es_client, max_suggestions=3)
        if movie_data:
            database_info = movie_data
        else:
            database_info = "Không tìm thấy thông tin trong database."
    except Exception as e:
        print(f"Database error in movie content query: {e}")
        database_info = "Lỗi khi truy vấn database."
    
    # Use specialized movie content prompt
    content_chain = MOVIE_CONTENT_TEMPLATE | llm
    
    content_response = content_chain.invoke({
        "movie_name": movie_name,
        "user_query": user_query,
        "recent_context": recent_context,
        "database_info": database_info
    })
    
    # Extract movie info from database if available
    tconsts = []
    movies = []
    
    if database_info and database_info != "Không tìm thấy thông tin trong database.":
        # Parse database info to extract tconsts and movie names
        import re
        tconst_matches = re.findall(r'_([a-z0-9]+)$', database_info, re.MULTILINE)
        movie_matches = re.findall(r'^([^_]+)_', database_info, re.MULTILINE)
        
        tconsts = tconst_matches[:3]  # Limit to top 3
        movies = movie_matches[:3]
    
    response_content = content_response.content if hasattr(content_response, 'content') else str(content_response)
    
    return {
        "message": response_content,
        "tconsts": tconsts,
        "movie": movies,
        "intent": "movie content",
        "context_used": f"Database: {len(database_info)} chars, LLM knowledge used"
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