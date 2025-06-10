# from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
QUERY_PROMPT = """
You are a friendly and helpful movie recommendation assistant. Based on the user request, you will find the intend of the user and convert the query into four types of query:
1. Search by movie name: "Movie name: <movie_name>". If user define specific movie series, you can return this type.
2. Search by description: "Description: <description>"
3. Choose a movie: "Choose a movie: <movie_name>"
4. Normal chat: "Chat: <query>"
User request:
{query}
You will return in the following format:
{{
  "query": "<your query text>"
  "type": "<query type>"
}}
If the query is not clear and not about movies, you should return:
{{
  "query": "No information",
  "type": "chat"
}}
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

CONSTRAINTS = """Your output must be in the following JSON format:
{{
  message: "<your natural language recommendation message with descrtiption of the each movies>",
  tconsts: ["<tconst1>", "<tconst2>", "..."],
  movie: ["<movie name 1>", "<movie name 2>", "..."],
  intent: "<query type, only one of the following: 'Search by movie name', 'Search by description', 'Choose a specific movie', 'Normal chat'>",
}}
Just return tconst and movie name if you find inside the context, do not use your own knowledge to find the movie, only use the information provided in the context.
"""

CONSTRAINTS_SYSTEM_PLACEHOLDER = ("system", f"Constraints: {CONSTRAINTS}")

CHAT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful movie assistant that uses tools to find information."),
    MessagesPlaceholder(variable_name="history"),
    ("system", "Relevant information: {context}"),
    CONSTRAINTS_SYSTEM_PLACEHOLDER,
    ("human", "{query}")   
])