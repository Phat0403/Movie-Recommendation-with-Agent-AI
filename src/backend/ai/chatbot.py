import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
import chromadb
from ai.embedder import Embedder # Import lớp Embedder của bạn
from utils.common_functions import read_yaml
from utils.logger import get_logger
import random
logger = get_logger(__name__)

# Tải các biến môi trường từ .env ở thư mục gốc src/
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

from db.clients import get_chroma_client

client = get_chroma_client()
# Khởi tạo mô hình Groq
llm = ChatGroq(model_name="llama3-8b-8192", temperature=0.7) # Hoặc llama3-70b-8192

# Biến toàn cục lưu danh sách phim đã gợi ý trong session hiện tại
seen_ids = set()

PROMPT_TEMPLATE = """
Bạn là một trợ lý đề xuất phim thân thiện và hữu ích. Dựa trên thông tin phim được cung cấp dưới đây và yêu cầu của người dùng, hãy đề xuất những bộ phim phù hợp từ dữ liệu chứa mô tả (description của bộ phim).

Lưu ý: Nếu có nhiều phim phù hợp, hãy ưu tiên đề xuất những phim chưa từng được nhắc đến trước đó (nếu có thể), nhằm tạo sự đa dạng. Tránh lặp lại những đề xuất trước đó.

Thông tin phim liên quan:
{context}

Yêu cầu của người dùng:
{question}

Đề xuất phim của bạn:
"""

def get_movie_recommendation(user_query: str, max_suggestions: int = 5) -> str:
    """
    Truy vấn ChromaDB để tìm phim liên quan và sử dụng LLM để tạo đề xuất,
    đồng thời tránh lặp lại các phim đã từng gợi ý.
    """
    results = client.query(
        query_text=user_query,
        n_results=25  # Lấy nhiều để có thể lọc + shuffle
    )

    # Kiểm tra có dữ liệu không
    documents = results.get('documents', [[]])[0]
    metadatas = results.get('metadatas', [[]])[0]
    ids = results.get('ids', [[]])[0]

    # Gộp lại thành danh sách tuple để xử lý dễ hơn
    combined = list(zip(documents, metadatas, ids))

    # Lọc ra các phim chưa được gợi ý trước đó
    unseen_movies = [item for item in combined if item[2] not in seen_ids]

    if not unseen_movies:
        return "Hiện tại tôi không tìm thấy phim nào mới để đề xuất. Vui lòng thử yêu cầu khác."

    # Xáo trộn để tăng tính đa dạng
    random.shuffle(unseen_movies)

    # Chọn số lượng tối đa cần thiết
    selected_movies = unseen_movies[:max_suggestions]

    # Cập nhật danh sách phim đã gợi ý
    for _, _, movie_id in selected_movies:
        seen_ids.add(movie_id)

    # Tạo context từ các phim đã chọn
    context_docs = []
    for doc_content, metadata, movie_id in selected_movies:
        title = metadata.get('name', 'N/A')
        genres = metadata.get('genres', metadata.get('genre', 'N/A'))
        description = doc_content or "No description available"

        context_str = (
            f"ID: {movie_id}\n"
            f"Title: {title}\n"
            f"Genres: {genres}\n"
            f"Description: {description}\n"
        )
        context_docs.append(context_str)

    context = "\n\n".join(context_docs)

    # Tạo prompt hoàn chỉnh
    formatted_prompt = PROMPT_TEMPLATE.format(context=context, question=user_query)

    # Gọi mô hình sinh văn bản
    try:
        chat_completion = llm.invoke(formatted_prompt)
        return chat_completion.content
    except Exception as e:
        logger.error(f"Đã xảy ra lỗi trong quá trình tạo phản hồi từ LLM: {e}")
        return f"Đã xảy ra lỗi: {e}"

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
    logger.info("Chào mừng bạn đến với Chatbot Đề xuất Phim! Gõ 'thoát' để dừng.")
    while True:
        user_input = input("Bạn muốn xem phim như thế nào? (Gõ 'thoát' để dừng): ")
        if user_input.lower() == "thoát":
            logger.info("Tạm biệt!")
            break

        response = get_movie_recommendation(user_input)
        logger.info(f"Chatbot: {response}")


if __name__ == "__main__":
    main()