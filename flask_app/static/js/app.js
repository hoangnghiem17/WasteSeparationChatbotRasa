document.getElementById("send-btn").addEventListener("click", function () {
    const userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    const messageDiv = document.createElement("div");
    messageDiv.textContent = "You: " + userInput;
    document.getElementById("messages").appendChild(messageDiv);

    // Send user's message as JSON (from input field) to Flask /chat endpoint
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    }) // Receives chatbot's response from Flask and displays it in conversation area
    .then(response => response.json())
    .then(data => {
        const botResponseDiv = document.createElement("div");
        if (data.error) {
            botResponseDiv.textContent = "Error: " + data.error;
        } else {
            botResponseDiv.textContent = "Bot: " + (data[0]?.text || "No response");
        }
        document.getElementById("messages").appendChild(botResponseDiv);
    })
    .catch(error => {
        const errorDiv = document.createElement("div");
        errorDiv.textContent = "Error: Unable to connect to the server.";
        document.getElementById("messages").appendChild(errorDiv);
    });

    // Clear input field
    document.getElementById("user-input").value = "";
});
