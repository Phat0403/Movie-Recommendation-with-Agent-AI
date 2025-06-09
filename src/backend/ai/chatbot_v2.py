import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from utils.logger import get_logger
import random
logger = get_logger(__name__)

# Tải các biến môi trường từ .env ở thư mục gốc src/
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

from db.clients import get_chroma_client

client = get_chroma_client()
# Khởi tạo mô hình Groq
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.6,
    max_output_tokens=1024
)

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



def get_movie_recommendation(user_query: str, max_suggestions: int = 20, history = "") -> str:
    """
    Truy vấn ChromaDB để tìm phim liên quan và sử dụng LLM để tạo đề xuất,
    đồng thời tránh lặp lại các phim đã từng gợi ý.
    """
    query_chain = QUERY_PROMPT_TEMPLATE | llm
    query_text = query_chain.invoke({"query": user_query}).content.strip()
    if query_text == "No information":
        return {
            "message": "Sorry, I am just a movie recommendation assistant, I cannot understand and answer your question.",
            "tconsts": [],
            "movie": []
        }
    print(f"Query text: {query_text}")
    query = query_text.split(": ")[1] if ": " in query_text else query_text
    results = client.query(
        query_text=query,
        n_results=max_suggestions  # Lấy nhiều để có thể lọc + shuffle
    )

    # Kiểm tra có dữ liệu không
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
import argparse
from utils.logger import get_logger
# import các module cần thiết...

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Câu hỏi từ dòng lệnh")
    args = parser.parse_args()

    if args.input:
        response = get_movie_recommendation(args.input)
        logger.info(f"Chatbot: {response}")

    else:
        interactive_loop()


def interactive_loop():
    history = ""
    while True:
        print("History of recommended movies:", history)
        user_input = input("Hi there! 👋 I'm here to help you with movie recommendations, answering questions, or anything else you need. What can I assist you with today: \n")
        if user_input.lower() == "exit":
            break
        
        response = get_movie_recommendation(user_input, history=history)
        history = response.get("history", "")
        logger.info(f"Chatbot: {response}")


if __name__ == "__main__":
    print(1)
    main()