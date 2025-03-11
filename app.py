from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from rag_pipeline import generate_response
from database import save_chat_history, fetch_chat_history
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)  # Allow frontend to access API

# Serve the chatbot UI
@app.route("/")
def home():
    return render_template("index.html")  # ✅ Ensure `index.html` exists in `templates/`

# Chatbot API endpoint
@app.route("/chat", methods=["POST"])
def chat():
    """Chatbot API for handling user messages with context memory."""
    data = request.get_json()

    # Handle missing input
    if not data or "message" not in data or not isinstance(data["message"], str):
        return jsonify({"response": "⚠️ Error: Invalid input."}), 400

    user_text = data["message"].strip()

    # Ensure user input is not empty
    if not user_text:
        return jsonify({"response": "⚠️ Error: Empty message."}), 400

    try:
        # Fetch past chat history for context
        chat_context = fetch_chat_history(limit=5)  # Get last 5 messages

        # Generate chatbot response with context
        bot_response = generate_response(user_text, chat_context)

        # Save conversation in database
        save_chat_history(user_text, bot_response)

        # Log interaction
        logging.info(f"User: {user_text} | Bot: {bot_response}")

        return jsonify({"response": bot_response})

    except Exception as e:
        logging.error(f"❌ ERROR in chatbot response: {e}")
        return jsonify({"response": "⚠️ Error: Chatbot is not responding. Please try again."}), 500

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
