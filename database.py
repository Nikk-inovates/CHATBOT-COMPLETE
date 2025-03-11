import psycopg2
from psycopg2 import sql
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Establish database connection
def connect_db():
    """Connects to PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        logging.error(f"❌ ERROR: Database connection failed: {e}")
        return None

# Create chat history table if not exists
def create_table():
    """Creates chat_history table if it does not exist."""
    conn = connect_db()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id SERIAL PRIMARY KEY,
                    user_message TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            logging.info("✅ Table 'chat_history' is ready.")
    except Exception as e:
        logging.error(f"❌ ERROR: Failed to create table: {e}")
    finally:
        conn.close()

# Save user and bot conversation
def save_chat_history(user_message, bot_response):
    """Saves user messages and bot responses to the database."""
    conn = connect_db()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO chat_history (user_message, bot_response) VALUES (%s, %s)",
                (user_message, bot_response),
            )
            conn.commit()
            logging.info("💾 Chat saved to database.")
    except Exception as e:
        logging.error(f"❌ ERROR: Failed to save chat: {e}")
    finally:
        conn.close()

# Fetch past chat history for context
def fetch_chat_history(limit=5):
    """Fetches the last 'limit' messages from chat history."""
    conn = connect_db()
    if not conn:
        return []

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT user_message, bot_response FROM chat_history ORDER BY timestamp DESC LIMIT %s",
                (limit,),
            )
            chat_history = cur.fetchall()  # Returns list of tuples [(user_msg, bot_msg), ...]
            return chat_history
    except Exception as e:
        logging.error(f"❌ ERROR: Failed to fetch chat history: {e}")
        return []
    finally:
        conn.close()

# Run table creation when script is executed
if __name__ == "__main__":
    create_table()
