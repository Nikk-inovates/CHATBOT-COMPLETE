import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API Key (Required)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ ERROR: GEMINI_API_KEY is not set. Check your .env file!")
