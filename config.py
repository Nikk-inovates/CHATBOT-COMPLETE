import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch API Key (Required)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ ERROR: GEMINI_API_KEY is missing! Please check your .env file and set the correct key.")

print("✅ GEMINI_API_KEY successfully loaded!")  # Debugging message (remove in production)

# Fetch Database Credentials (Required)
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Validate Database Credentials
if not all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT]):
    raise ValueError("❌ ERROR: One or more database credentials are missing! Check your .env file.")

print(f"✅ Successfully loaded database credentials for '{DB_NAME}'")  # Debugging message
