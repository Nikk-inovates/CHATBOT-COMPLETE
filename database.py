import os
import psycopg2
from psycopg2.extras import RealDictCursor

# ✅ Fetch Database URL from Render Environment Variables
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Establish a connection to PostgreSQL database."""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def save_chat_history(user_text, bot_response):
    """Save chat history to PostgreSQL."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO chatbot_dialogs (user_text, bot_text) VALUES (%s, %s)", 
                    (user_text, bot_response))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Database Error: {e}")

def fetch_chat_history(limit=5):
    """Fetch last few chat messages for context."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_text, bot_text FROM chatbot_dialogs ORDER BY id DESC LIMIT %s", (limit,))
        chat_history = cur.fetchall()
        cur.close()
        conn.close()
        return chat_history
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return []
