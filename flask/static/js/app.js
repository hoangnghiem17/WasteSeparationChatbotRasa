// Adds click and press event listener to button with id "send-btn" and retrieves value from input field with id "user-input"
document.getElementById("send-btn").addEventListener("click", handleSend);

document.getElementById("user-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        handleSend();
    }
});

function handleSend() {
    const userInput = document.getElementById("user-input").value;
    if (!userInput) {
        console.warn("No user input provided.");
        return;
    }
    console.log("User input:", userInput);

// Display user message in chat window    
    const messageDiv = document.createElement("div"); // creates new <div> element to display user's message
    messageDiv.textContent = "You: " + userInput; // Showing content newly created with prefix "You: "
    document.getElementById("messages").appendChild(messageDiv); // Adds user's message to <div> with id "messages" to chatbot interface

    // Send user's message as JSON (from input field) to Backend (Flask /chat endpoint)
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    }) // Receives chatbot's response from Flask and displays it in conversation area
    .then(response => response.json()) // Converts server's response into a JSON object
    .then(data => {
        console.log("Received response from backend:", data);
        const botResponseDiv = document.createElement("div"); // Create new <div> element to display chat's response
        if (data.error) {
            console.error("Error from backend:", data.error);
            botResponseDiv.textContent = "Error: " + data.error;
        } else {
            botResponseDiv.textContent = "Bot: " + (data[0]?.text || "No response"); // Display bot's response
        }
        document.getElementById("messages").appendChild(botResponseDiv); // Add bot's response to <div> with id "messages" to chatbot interface
    }) // Handles errors during fetch operation
    .catch(error => {
        console.error("Error connecting to backend:", error);
        const errorDiv = document.createElement("div");
        errorDiv.textContent = "Error: Unable to connect to the server.";
        document.getElementById("messages").appendChild(errorDiv);
    });

    // Clear input field after sending message
    document.getElementById("user-input").value = "";
    console.log("Cleared input field after sending message.");
};
