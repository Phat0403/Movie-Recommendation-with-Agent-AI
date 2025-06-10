from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import List
from db.clients import get_chroma_client, get_es_client
from config.config import Settings
from pydantic import BaseModel
import asyncio

# ======= Setup config & clients =======
setting = Settings()
client = get_chroma_client()
es_client = get_es_client()
es_client.connect()

# ======= Pydantic Input Models =======
class QueryInput(BaseModel):
    query: str
    limit: int = 10

class MovieSearchInput(BaseModel):
    movie_name: str
    limit: int = 10

# ======= Tools =======
@tool(args_schema=QueryInput)
def search_by_query(query: str, limit: int = 10) -> str:
    """
    Search vector DB with a text query and return matching movie titles and IDs.
    """
    results = client.query(query_text=query, n_results=limit)
    documents = results.get('documents', [[]])[0]
    ids = results.get('ids', [[]])[0]
    return "\n".join(f"{doc}_{ids[i]}" for i, doc in enumerate(documents[:limit]))

@tool(args_schema=MovieSearchInput)
async def search_by_movie_name(movie_name: str, limit: int = 10) -> str:
    """
    Fuzzy search movie titles in Elasticsearch index and return matched results.
    """
    results = await es_client.fuzzy_search(
        index="movies",
        field="title",
        value=movie_name,
        size=limit
    )
    documents = results.get('hits', {}).get('hits', [])
    return "\n".join(f"{doc['_source']['title']}_{doc['_id']}" for doc in documents)


# ======= Language model =======
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
    api_key=setting.GOOGLE_API_KEY,
)

# ======= Tool list =======
tools = [search_by_query, search_by_movie_name]

# ======= Prompt for StructuredChatAgent =======
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful movie assistant that uses tools to find information."),
    ("system", "Available tools: {tools}"),
    ("system", "Tool names: {tool_names}"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad")
])

# ======= Agent creation =======
agent = create_structured_chat_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# ======= Run async agent =======
async def main():
    query = "Find me movie name Spider-man"
    print(type(query))  # phải là str
    response = await agent_executor.ainvoke({"input": query})
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
