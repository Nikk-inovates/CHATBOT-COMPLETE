document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    // Function to add a message to the chat with animation
    function addMessage(text, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");
        messageDiv.innerHTML = `<strong>${sender === "user" ? "You" : "Bot"}:</strong> ${text}`;
        chatBox.appendChild(messageDiv);

        // Auto-scroll to the latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Function to send user message
    function sendMessage() {
        const userMessage = userInput.value.trim();
        if (userMessage === "") {
            alert("⚠️ Please enter a message!");
            return;
        }

        // Display user message
        addMessage(userMessage, "user");

        // Show "Typing..." message while waiting for response
        const botTyping = document.createElement("div");
        botTyping.classList.add("message", "bot-message");
        botTyping.innerHTML = `<strong>Bot:</strong> ⏳ Typing...`;
        chatBox.appendChild(botTyping);
        chatBox.scrollTop = chatBox.scrollHeight;

        // Send request to Flask API
        fetch("https://chatbot-complete.onrender.com/chat", { // ✅ Correct API endpoint
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            // Remove "Typing..." message
            chatBox.removeChild(botTyping);

            // Display chatbot response
            addMessage(data.response, "bot");
        })
        .catch(error => {
            console.error("❌ ERROR:", error);
            chatBox.removeChild(botTyping);
            addMessage("⚠️ Error: Chatbot is not responding.", "bot");
        });

        // Clear input field
        userInput.value = "";
    }

    // Send button event listener
    sendBtn.addEventListener("click", sendMessage);

    // Enter key event listener
    userInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});
