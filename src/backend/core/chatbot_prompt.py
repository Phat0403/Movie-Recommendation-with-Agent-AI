from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

# -------- QUERY PROMPT --------
QUERY_PROMPT = """
Ngữ cảnh hội thoại gần đây: {history}

Bạn là trợ lý gợi ý phim thông minh. Dựa trên ngữ cảnh hội thoại gần đây và yêu cầu của người dùng, hãy xác định ý định và chuyển đổi truy vấn thành một trong các loại sau:

1. **Chọn phim cụ thể** → Format: "Choose a movie: <tên_phim>"  
2. **Tìm kiếm theo tên phim** → Format: "Movie name: <tên_phim>"  
3. **Tìm kiếm theo mô tả** → Format: "Description: <mô_tả>"  
4. **Hỏi về nội dung phim** → Format: "Movie content: <tên_phim>"
5. **Trò chuyện thường** → Format: "Chat: <câu_hỏi>"  

**Hướng dẫn phân loại:**
- Nếu người dùng hỏi về nội dung, cốt truyện, diễn viên của một phim cụ thể → "Movie content"
- Nếu người dùng muốn chọn một phim từ danh sách đã thảo luận → "Choose a movie"  
- Nếu người dùng tìm phim theo tên cụ thể → "Movie name"
- Nếu người dùng mô tả thể loại, tâm trạng, chủ đề → "Description"
- Các câu hỏi khác → "Chat"

**Quan trọng:** Hãy sử dụng ngữ cảnh hội thoại gần đây để hiểu rõ hơn ý định của người dùng.

Trả về CHÍNH XÁC một JSON object (không có markdown, không có giải thích):

{{
  "query": "<văn bản truy vấn của bạn>",
  "type": "<một trong: 'Search by movie name', 'Search by description', 'Choose a movie', 'Movie content', 'Normal chat'>"
}}

Yêu cầu của người dùng:
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
- Sử dụng CHÍNH XÁC thông tin từ context và lịch sử hội thoại để trích xuất hoặc gợi ý phim.
- Khi không có thông tin trong database, sử dụng kiến thức chung về phim để trả lời.
- Ưu tiên ngữ cảnh hội thoại gần đây để hiểu rõ ý định người dùng.
- Trả lời bằng tiếng Việt với tông điệu thân thiện và hữu ích.
- CHỈ trả về JSON object hợp lệ. KHÔNG sử dụng markdown code blocks như ```json.
- KHÔNG bao gồm giải thích hoặc văn bản bổ sung.

Format mong đợi:
{{
  "message": "<tin nhắn gợi ý bằng tiếng Việt với tông điệu thân thiện>",
  "tconsts": ["<tconst1>", "..."],
  "movie": ["<tên phim>", "..."],
  "intent": "<loại truy vấn>"
}}
"""

CHAT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Bạn là trợ lý thông minh chuyên về phim ảnh, sử dụng các công cụ để tìm kiếm thông tin và hỗ trợ người dùng."),
    MessagesPlaceholder(variable_name="history"),
    ("system", "Ngữ cảnh hội thoại gần đây: {recent_context}"),
    ("system", "Thông tin liên quan: {context}"),
    ("system", f"Hướng dẫn: {CONSTRAINTS}"),
    ("human", "{query}")
])

# -------- NEW: Movie Content Prompt --------
MOVIE_CONTENT_PROMPT = """
Người dùng hỏi về nội dung phim: {movie_name}
Câu hỏi cụ thể: {user_query}
Ngữ cảnh hội thoại: {recent_context}

Thông tin có sẵn từ database:
{database_info}

Hãy trả lời câu hỏi của người dùng về phim này. Nếu thông tin từ database không đủ, 
hãy sử dụng kiến thức chung về phim để bổ sung thông tin hữu ích.

Bao gồm các thông tin như:
- Nội dung/cốt truyện chính
- Diễn viên và đạo diễn
- Thể loại và năm phát hành  
- Đánh giá hoặc điểm đặc biệt
- Thông tin liên quan đến câu hỏi cụ thể

Trả lời bằng tiếng Việt, tự nhiên và thân thiện.
"""

MOVIE_CONTENT_TEMPLATE = PromptTemplate(
    input_variables=["movie_name", "user_query", "recent_context", "database_info"],
    template=MOVIE_CONTENT_PROMPT
)

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
