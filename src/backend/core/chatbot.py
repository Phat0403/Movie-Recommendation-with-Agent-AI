from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from db.clients import get_chroma_client
from config.config import Settings

settings = Settings()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    max_output_tokens=1024,
    api_key=settings.GOOGLE_API_KEY
)
client = get_chroma_client()

QUERY_PROMPT = """
You are a friendly and helpful movie recommendation assistant. Based on the user request, rewrite the query more descriptive to make it more suitable for searching in a movie vector database.
User request:
{query}
You only return the query text without any additional explanation or formatting. Only return the text. If the query is not clear and not about movies, you should return "No information"
"""

QUERY_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["query"],
    template=QUERY_PROMPT
)

RECOMMEND_PROMPT = """
Previously recommended movies:
{history}

You are a friendly and helpful movie recommendation assistant. Based on the movie information provided below and the user's request, suggest suitable movies for them

Note:
- If multiple movies match the request, prioritize recommending ones that have not been mentioned in history to ensure diversity if possible.
- If you do not see any movies that match the request, you can say you can not find the movie the user are looking for but can suggest some movies that are similar to the request.

Relevant movie information:
{context}

User request:
{query}

Your output must be in the following JSON format:
{{
  message: "<your natural language recommendation message with descrtiption of the each movies>",
  tconsts: ["<tconst1>", "<tconst2>", "..."],
  movie: ["<movie name 1>", "<movie name 2>", "..."],
  history: "<your history of recommended movies that you have metioned in the movie list mix with old history, separated by commas, only include names of movies that you have metioned in the output>"
}}
"""

RECOMMEND_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["context", "query", "history"],
    template=RECOMMEND_PROMPT
)

def get_movie_recommendation(user_query: str, history: str = "", max_suggestions: int = 15) -> str:
    """
    Retrieve movie recommendations based on user query and history.
    Uses ChromaDB to find relevant movies and LLM to generate recommendations.
    """
    query_chain = QUERY_PROMPT_TEMPLATE | llm
    query_text = query_chain.invoke({"query": user_query}).content.strip()
    query_text = query_text.split(": ")[1] if ": " in query_text else query_text
    if query_text == "No information":
        return {
            "message": "Sorry, I am just a movie recommendation assistant, I cannot understand and answer your question.",
            "tconsts": [],
            "movie": [],
            "history": history
        }
    results = client.query(
        query_text=query_text,
        n_results= max_suggestions
    )

    documents = results.get('documents', [[]])[0]
    ids = results.get('ids', [[]])[0]
    texts = []
    for i in range(max_suggestions):
        text = documents[i]+"_"+str(ids[i])
        texts.append(text)

    texts = "\n".join(texts)

    recommend_chain = RECOMMEND_PROMPT_TEMPLATE | llm | JsonOutputParser()
    response = recommend_chain.invoke({
        "context": texts,
        "query": user_query,
        "history": history
    })
    return response