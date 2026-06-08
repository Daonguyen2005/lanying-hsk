import google.genai as genai
from google.genai import types
from config import GEMINI_API_KEY
import os

# Tải knowledge base từ file txt
def load_knowledge_base() -> str:
    kb_path = os.path.join(os.path.dirname(__file__), "..", "..", "database", "knowledge_base", "hsk_grammar.txt")
    try:
        with open(kb_path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "Tài liệu ngữ pháp HSK đang được cập nhật."

KNOWLEDGE_BASE = load_knowledge_base()

def chat_with_rag(user_question: str) -> str:
    """
    RAG đơn giản: Ghép knowledge base + câu hỏi vào prompt rồi gọi Gemini API.
    """
    prompt = f"""Bạn là trợ lý AI của nền tảng gia sư tiếng Trung Lanying HSK.
Nhiệm vụ của bạn là tư vấn học tiếng Trung và giải đáp ngữ pháp HSK dựa trên tài liệu dưới đây.
Nếu câu hỏi không liên quan đến tiếng Trung, hãy lịch sự từ chối và hướng người dùng đặt lịch với gia sư.

=== TÀI LIỆU THAM KHẢO ===
{KNOWLEDGE_BASE[:3000]}
=========================

Câu hỏi của học viên: {user_question}

Trả lời bằng tiếng Việt, ngắn gọn, dễ hiểu:"""

    try:
        # Khởi tạo client lazy - chỉ tạo khi cần dùng
        if not GEMINI_API_KEY:
            return "Xin chào! Hiện tại hệ thống AI chưa được cấu hình. Vui lòng liên hệ admin."
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return "Xin chào! Hiện tại hệ thống AI đang bảo trì (vượt quá giới hạn API miễn phí trong ngày). Tuy nhiên, nền tảng gia sư Lanying HSK của chúng tôi vẫn hoạt động bình thường. Bạn có muốn tìm hiểu về lộ trình học hay xem danh sách gia sư không?"
