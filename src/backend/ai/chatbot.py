import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
import chromadb
from ai.embedder import Embedder # Import lớp Embedder của bạn
from utils.common_functions import read_yaml
from utils.logger import get_logger

logger = get_logger(__name__)

# Tải các biến môi trường từ .env ở thư mục gốc src/
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

from db.clients import get_chroma_client

client = get_chroma_client()
# Khởi tạo mô hình Groq
llm = ChatGroq(model_name="llama3-8b-8192", temperature=0.7) # Hoặc llama3-70b-8192

# Định nghĩa prompt cho chatbot
PROMPT_TEMPLATE = """
Bạn là một trợ lý đề xuất phim thân thiện và hữu ích. Dựa trên thông tin phim được cung cấp dưới đây và yêu cầu của người dùng, hãy đề xuất những bộ phim phù hợp từ dữ liệu chứa mô tả (description của bộ phim).
Nếu bạn không tìm thấy phim nào liên quan hoặc không đủ thông tin, hãy nói rằng bạn không thể đề xuất cụ thể và mời người dùng cung cấp thêm chi tiết.

Thông tin phim liên quan:
{context}

Yêu cầu của người dùng:
{question}

Đề xuất phim của bạn:
"""

def get_movie_recommendation(user_query: str) -> str:
    """
    Truy vấn ChromaDB để tìm phim liên quan và sử dụng Groq để tạo đề xuất.
    """
    # LangChain Chroma connector cần một object của VectorStore,
    # chúng ta sẽ tạo nó từ collection hiện có.
    # Tuy nhiên, RetrievalQA của LangChain thường hoạt động với một retriever trực tiếp.
    # Chúng ta sẽ sử dụng trực tiếp collection của ChromaDB và LangChain để ghép nối.

    # Tìm kiếm các tài liệu liên quan trong ChromaDB
    # Use embedder_instance.embed_query for the user query
    # Tìm kiếm trong ChromaDB, trả về documents (page_content) và metadatas
    results = client.query(
        query_text=user_query, # query_text nên là query_texts vì nó mong đợi một danh sách
        n_results=10  # Số lượng kết quả muốn lấy
    )

    # Trích xuất nội dung từ kết quả tìm kiếm để làm context cho LLM
    context_docs = []
    if results['documents']:
        for i, doc_content in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            # Tạo một chuỗi context tốt hơn từ metadata và content
            context_str = f"Title: {metadata.get('name', 'N/A')}\n" # Giả định metadata có 'name'
            if doc_content: # doc_content là movie_description đã nhúng
                context_str += f"Description: {doc_content}\n" # Dòng đã sửa: sử dụng trực tiếp doc_content
            # Thêm các metadata khác nếu muốn (ví dụ: genre, director)
            # context_str += f"Genre: {metadata.get('genre', 'N/A')}\n"
            context_docs.append(context_str)
    
    context = "\n\n".join(context_docs) if context_docs else "Không tìm thấy thông tin phim liên quan."

    # Định dạng prompt
    formatted_prompt = PROMPT_TEMPLATE.format(context=context, question=user_query)

    try:
        # Gửi prompt đã định dạng đến Groq LLM
        chat_completion = llm.invoke(formatted_prompt)
        answer = chat_completion.content
        return answer
    except Exception as e:
        logger.error(f"Đã xảy ra lỗi trong quá trình tạo phản hồi từ LLM: {e}")
        return f"Đã xảy ra lỗi: {e}"

if __name__ == "__main__":
    logger.info("Chào mừng bạn đến với Chatbot Đề xuất Phim! Gõ 'thoát' để dừng.")
    while True:
        user_input = input("Bạn muốn xem phim như thế nào? (Gõ 'thoát' để dừng): ")
        if user_input.lower() == "thoát":
            logger.info("Tạm biệt!")
            break
        
        response = get_movie_recommendation(user_input)
        logger.info(f"Chatbot: {response}")