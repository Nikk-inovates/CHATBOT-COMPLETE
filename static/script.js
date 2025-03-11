document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    // ✅ API Endpoint (Replace with your actual Render URL)
    const API_URL = "https://chatbot-complete.onrender.com/chat";  

    // ✅ Function to add a message to the chat UI
    function addMessage(text, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");
        messageDiv.innerHTML = `<strong>${sender === "user" ? "You" : "Bot"}:</strong> ${text}`;
        chatBox.appendChild(messageDiv);

        // ✅ Auto-scroll to latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // ✅ Function to send user message
    function sendMessage() {
        const userMessage = userInput.value.trim();
        if (!userMessage) {
            alert("⚠️ Please enter a message!");
            return;
        }

        // ✅ Display user message
        addMessage(userMessage, "user");

        // ✅ Show "Typing..." message
        const botTyping = document.createElement("div");
        botTyping.classList.add("message", "bot-message", "typing");
        botTyping.innerHTML = `<strong>Bot:</strong> ⏳ Typing...`;
        chatBox.appendChild(botTyping);
        chatBox.scrollTop = chatBox.scrollHeight;

        // ✅ Send request to Flask API
        fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            chatBox.removeChild(botTyping); // ✅ Remove "Typing..." message
            addMessage(data.response || "⚠️ No response received.", "bot");
        })
        .catch(error => {
            console.error("❌ ERROR:", error);
            chatBox.removeChild(botTyping);
            addMessage("⚠️ Error: Chatbot is not responding.", "bot");
        });

        // ✅ Clear input field after sending
        userInput.value = "";
    }

    // ✅ Send button event listener
    sendBtn.addEventListener("click", sendMessage);

    // ✅ Enter key event listener
    userInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});
