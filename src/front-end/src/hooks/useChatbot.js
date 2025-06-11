// Base URL for your FastAPI backend. Adjust if necessary.
const API_BASE_URL = 'http://localhost:8000/api/chatbot'; // Assuming same origin

// Kiểm tra trạng thái dịch vụ chat
function isChatServiceActive() {
  // Giả định API đang hoạt động nếu frontend đang chạy
  return true;
}

// Khởi tạo cuộc hội thoại mới từ API
async function initConversation() {
  try {
    const response = await fetch(`${API_BASE_URL}/init-conversation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // body: JSON.stringify({}) // Bỏ comment nếu API yêu cầu body rỗng
    });

    if (!response.ok) {
      const errorData = await response.text();
      throw new Error(`API error (${response.status}): ${errorData || response.statusText}`);
    }

    // Trả về JSON với khóa conversation_id
    return await response.json();
  } catch (error) {
    console.error("Error initializing conversation:", error);
    throw error;
  }
}

// Gửi tin nhắn và nhận phản hồi từ bot
async function postMessage(conversationId, messageText) {
  if (!conversationId) {
    throw new Error("Conversation ID is missing.");
  }

  try {
    const response = await fetch(`${API_BASE_URL}/response-message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        conversation_id: conversationId,
        message: messageText,
      }),
    });

    if (!response.ok) {
      const errorData = await response.text();
      throw new Error(`API error (${response.status}): ${errorData || response.statusText}`);
    }

    // Trả về JSON với conversation_id và messages
    return await response.json();
  } catch (error) {
    console.error("Error posting message:", error);
    throw error;
  }
}
export { initConversation, postMessage };