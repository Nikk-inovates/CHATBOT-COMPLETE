import google.generativeai as genai
import pdfplumber
import os
import logging
from config import GEMINI_API_KEY

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)

# ✅ Configure Google Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
GEMINI_MODEL = "gemini-1.5-flash"

# ✅ Define Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_FOLDER = os.path.join(BASE_DIR, "data", "documents")  # Folder where PDFs are stored

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
        logging.warning("⚠️ No PDF files found in the 'documents' folder.")
        return None

    # ✅ Select the first PDF file found
    pdf_path = os.path.join(DOCS_FOLDER, pdf_files[0])
    logging.info(f"📄 Extracting text from: {pdf_path}")
    return extract_text_from_pdf(pdf_path)

def generate_response(user_query):
    """Generate chatbot response using Gemini AI with PDF context."""
    
    # ✅ Load the PDF text
    pdf_context = load_pdf_context()
    
    # ✅ Construct prompt for Gemini AI
    prompt = f"""
    You are an AI assistant that answers questions based on the provided document.

    Document Content:
    {pdf_context}

    User: {user_query}
    AI Assistant:
    """

    try:
        # ✅ Use Google Gemini AI to generate response
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content([prompt])

        return response.text.strip() if response else "⚠️ AI is unavailable."

    except Exception as e:
        logging.error(f"❌ ERROR: Gemini API request failed: {e}")
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
