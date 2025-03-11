import google.generativeai as genai
import os

# ✅ Load Gemini API Key from environment variables
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_MODEL = "gemini-pro"

def load_pdf_context():
    """Load text from PDF for chatbot knowledge."""
    pdf_path = "documents/chatbot_knowledge.pdf"
    if not os.path.exists(pdf_path):
        return "⚠️ No documents available for reference."

    with open(pdf_path, "rb") as pdf_file:
        pdf_text = pdf_file.read().decode("utf-8")  # Extract text
        return pdf_text[:4000]  # Limit context size

def generate_response(user_query, chat_history=None):
    """Generate chatbot response with RAG model."""

    pdf_context = load_pdf_context()  # Load PDF text

    if not pdf_context or "⚠️" in pdf_context:
        return "⚠️ No documents available for reference."

    prompt = f"""
    You are an AI assistant answering based on the document.

    Document:
    {pdf_context}

    Chat History:
    {chat_history if chat_history else "No past conversations available."}

    User: {user_query}
    AI:
    """

    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content([prompt])

    return response.text.strip() if response else "⚠️ AI is unavailable."
