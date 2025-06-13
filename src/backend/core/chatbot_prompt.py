from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

# -------- QUERY PROMPT --------
QUERY_PROMPT = """
Your chat history: {history}
You are a friendly and helpful movie recommendation assistant. Based on the user request, determine the intent and transform the query into one of the following types:

1. Choose a specific movie → Format: "Choose a movie: <movie_name>"  
2. Search by movie name → Format: "Movie name: <movie_name>"  
3. Search by description → Format: "Description: <description>"  
4. Normal chat → Format: "Chat: <query>"  

Return only a JSON object (no markdown, no explanations):

{{
  "query": "<your query text>",
  "type": "<one of: 'Search by movie name', 'Search by description', 'Choose a specific movie', 'Normal chat'>"
}}
Do not say anything else.
Do not include explanation.
Return ONLY a valid JSON object in the specified format.
Type should be one of the following:
- "Search by movie name"
- "Search by description"
- "Choose a specific movie"
- "Normal chat"

User request:
{query}
"""

QUERY_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["query", "history"],
    template=QUERY_PROMPT
)

# -------- RECOMMEND PROMPT --------
RECOMMEND_PROMPT = """
Previously recommended movies:
{history}

You are a friendly and helpful movie recommendation assistant. Based on the movie information provided below and the user's request, suggest suitable movies.

Guidelines:
- Prioritize movies not yet mentioned in history.
- Only use info from context and history. Do not invent.
- If no match, suggest similar ones from context.

Relevant movie information:
{context}

User request:
{query}

Return only a valid JSON object (no markdown):

{{
  "message": "<natural language recommendation with descriptions>",
  "tconsts": ["<tconst1>", "<tconst2>", "..."],
  "movie": ["<movie name 1>", "<movie name 2>", "..."],
  "history": "<comma-separated names of movies you mentioned>"
}}
"""

RECOMMEND_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["context", "query", "history"],
    template=RECOMMEND_PROMPT
)

# -------- CONSTRAINTS for CHAT_PROMPT --------
CONSTRAINTS = """
- Use only context and history to extract or recommend movie information.
- Return one intent: 'Search by movie name', 'Search by description', 'Choose a specific movie', 'Normal chat'.
- Only return a valid JSON object. Do NOT use markdown code blocks like ```json.
- Do NOT include explanations or additional text.

Expected format:
{{
  "message": "<recommendation message>",
  "tconsts": ["<tconst1>", "..."],
  "movie": ["<movie name>", "..."],
  "intent": "<query type>"
}}
"""

CHAT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful movie assistant that uses tools to find information."),
    MessagesPlaceholder(variable_name="history"),
    ("system", "Relevant information: {context}"),
    ("system", f"Constraints: {CONSTRAINTS}"),
    ("human", "{query}")
])

# -------- Example Chain Usage --------
# llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# query_chain = LLMChain(llm=llm, prompt=QUERY_PROMPT_TEMPLATE)
# recommend_chain = LLMChain(llm=llm, prompt=RECOMMEND_PROMPT_TEMPLATE)

# # -------- Helper to clean any markdown-blocked JSON --------
# def clean_json_output(output: str):
#     output = output.strip()
#     if output.startswith("```json"):
#         output = re.sub(r"```json\s*([\s\S]+?)\s*```", r"\1", output.strip())
#     return json.loads(output)

# # -------- Example call --------
# if __name__ == "__main__":
#     history = "Previously: Not Friends_, Long Story Short_"
#     query = "I'm looking for a movie about deep friendship"
#     context = """
#     Not Friends_ [tt28937890]: A group of high school students who dream of making films set out to make a short film...
#     Long Story Short_ [tt33350035]: A group of close friends celebrate parties over an extended period of time...
#     """

#     # Step 1: Identify query type
#     query_result = query_chain.run({"query": query, "history": history})
#     print("Query Result (raw):", query_result)
#     parsed_query = clean_json_output(query_result)
#     print("Parsed:", parsed_query)

#     # Step 2: Recommend movie
#     recommend_result = recommend_chain.run({
#         "query": query,
#         "context": context,
#         "history": history
#     })
#     print("Recommend Result (raw):", recommend_result)
#     parsed_recommend = clean_json_output(recommend_result)
#     print("Parsed:", parsed_recommend)
