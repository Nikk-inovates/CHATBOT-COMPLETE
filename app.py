from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from rag_pipeline import generate_response
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app, resources={r"/chat": {"origins": "*"}})  # ✅ Allow all frontend requests to /chat

# Serve the chatbot UI
@app.route("/")
def home():
    return render_template("index.html")  # ✅ Ensure `index.html` exists in `templates/`

# Chatbot API endpoint
@app.route("/chat", methods=["POST"])
def chat():
    """Chatbot API for handling user messages."""
    try:
        data = request.get_json()

        # Handle missing or invalid input
        if not data or "message" not in data or not isinstance(data["message"], str):
            return jsonify({"response": "⚠️ Error: Invalid input."}), 400

        user_text = data["message"].strip()

        # Ensure user input is not empty
        if not user_text:
            return jsonify({"response": "⚠️ Error: Empty message."}), 400

        # Generate chatbot response
        bot_response = generate_response(user_text)
        logging.info(f"User: {user_text} | Bot: {bot_response}")  # Logs each interaction
        return jsonify({"response": bot_response})

    except Exception as e:
        logging.error(f"❌ ERROR in chatbot response: {e}")
        return jsonify({"response": "⚠️ Error: Chatbot is not responding. Please try again."}), 500

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
