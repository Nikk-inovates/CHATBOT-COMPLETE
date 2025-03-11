import google.generativeai as genai
import pdfplumber
import os
import logging
from config import GEMINI_API_KEY
from database import save_chat_history, fetch_chat_history
from deep_translator import GoogleTranslator

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)

# ✅ Configure Google Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
GEMINI_MODEL = "gemini-1.5-flash"

# ✅ Define Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_FOLDER = os.path.join(BASE_DIR, "data", "documents")  # Folder where PDFs are stored

# ✅ Ensure API Key is loaded
if not GEMINI_API_KEY:
    raise ValueError("❌ ERROR: GEMINI_API_KEY is missing! Add it in '.env' or Render Env Vars.")

# ✅ Ensure document folder exists
if not os.path.exists(DOCS_FOLDER):
    logging.error(f"❌ ERROR: Documents folder not found: {DOCS_FOLDER}")
    raise FileNotFoundError(f"❌ Documents folder missing: {DOCS_FOLDER}")

# ✅ Translator for Hindi-English support
translator = GoogleTranslator(source="auto", target="en")
reverse_translator = GoogleTranslator(source="en", target="auto")

def extract_text_from_pdf(pdf_path):
    """Extract text from a single PDF file."""
    extracted_text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)
        return " ".join(extracted_text) if extracted_text else None
    except Exception as e:
        logging.error(f"❌ ERROR: Failed to read PDF: {pdf_path} | {e}")
        return None

def load_pdf_context():
    """Load text from the first available PDF in the documents folder."""
    pdf_files = [f for f in os.listdir(DOCS_FOLDER) if f.endswith(".pdf")]

    if not pdf_files:
        logging.warning("⚠️ No PDF files found in 'documents' folder.")
        return "⚠️ No documents available."

    # ✅ Select the first PDF file found
    pdf_path = os.path.join(DOCS_FOLDER, pdf_files[0])
    logging.info(f"📄 Extracting text from: {pdf_path}")

    return extract_text_from_pdf(pdf_path)

def generate_response(user_message):
    """
    Generates chatbot responses using Gemini AI with chat history and document context.
    """
    try:
        # ✅ Detect language & translate if needed
        detected_lang = translator.detect(user_message)
        if detected_lang != "en":
            user_message = translator.translate(user_message)

        # ✅ Fetch last 5 messages for chat context
        chat_history = fetch_chat_history(limit=5)
        context = "\n".join([f"User: {u}\nBot: {b}" for u, b in chat_history])

        # ✅ Load document context
        pdf_context = load_pdf_context()
        if not pdf_context or "⚠️" in pdf_context:
            pdf_context = "⚠️ No documents available."

        # ✅ Construct prompt for Gemini AI
        prompt = f"""
        You are an AI assistant answering questions based on the provided conversation and document.

        Chat History:
        {context}

        Document Content:
        {pdf_context}

        User: {user_message}
        AI Assistant:
        """

        # ✅ Generate response from Gemini AI
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content([prompt])
        bot_response = response.text.strip() if response else "⚠️ AI is unavailable."

        # ✅ Translate back to Hindi if needed
        if detected_lang != "en":
            bot_response = reverse_translator.translate(bot_response)

        # ✅ Save chat history to database
        save_chat_history(user_message, bot_response)

        logging.info(f"User: {user_message} | Bot: {bot_response}")
        return bot_response

    except Exception as e:
        logging.error(f"❌ ERROR: Failed to generate response: {e}")
        return "⚠️ AI is currently unavailable. Please try again later."

# ✅ Test chatbot in terminal
if __name__ == "__main__":
    while True:
        user_input = input("\n📝 Enter your question (or type 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            print("👋 Exiting chatbot. Have a great day!")
            break

        bot_reply = generate_response(user_input)
        print("\n🤖 Chatbot Response:", bot_reply)
