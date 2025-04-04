document.addEventListener("DOMContentLoaded", function () {
    const inputField = document.getElementById("chatInput");
    const sendButton = document.getElementById("sendButton");
    const chatBox = document.getElementById("chatBox");
    const MAX_MESSAGE_LENGTH = 500; // Limit long messages

    // Disable send button if input is empty
    function updateSendButtonState() {
        sendButton.disabled = inputField.value.trim() === "";
    }

    // Listen for input changes
    inputField.addEventListener("input", updateSendButtonState);

    // Send message when the button is clicked
    sendButton.addEventListener("click", function () {
        sendButton.disabled = true; // Disable immediately to prevent spamming
        sendMessage();
    });

    // Allow sending messages with Enter key, prevent form submission
    inputField.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey && !sendButton.disabled) {
            event.preventDefault(); // Prevents default form submission
            sendMessage();
        }
    });

    // Function to send a message
    function sendMessage() {
        let message = inputField.value.trim();
        if (message.length > MAX_MESSAGE_LENGTH) {
            message = message.substring(0, MAX_MESSAGE_LENGTH) + "…"; // Truncate long messages
        }
        if (message !== "") {
            addMessage(message, "user");  // Add the user's message
            inputField.value = "";        // Clear input field
            updateSendButtonState();      // Ensure button state updates
            inputField.disabled = true;   // Disable input field while waiting for response
            sendButton.disabled = true;   // Disable send button
            sendToBackend(message);       // Send message to backend
        }
    }

    // Function to add a message to the chat
    function addMessage(text, sender) {
        const messageBubble = document.createElement("div");
        messageBubble.classList.add("message");
        messageBubble.classList.add(sender);

        if (sender === "bot") {
            const profilePic = document.createElement("img");
            profilePic.classList.add("arina-profile-pic"); // Unique class for Arina's profile picture
            profilePic.src = "arina-ui/images/arina.jpg"; // Arina's profile picture

            messageBubble.appendChild(profilePic); // Add Arina's profile picture to the chat bubble
        }

        const messageText = document.createElement("span");
        messageText.innerHTML = DOMPurify.sanitize(marked.parse(text)); // Convert Markdown safely
        messageBubble.appendChild(messageText);

        chatBox.appendChild(messageBubble);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Function to send message to backend
    async function sendToBackend(message) {
        try {
            const response = await fetch("http://localhost:8000/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            addMessage(data.response, "bot");
        } catch (error) {
            addMessage("⚠️ Connection error! Arina might be offline.", "error");
        } finally {
            inputField.disabled = false; // Always enable input field
            sendButton.disabled = false; // Ensure button is re-enabled
            updateSendButtonState();
        }        
    }

    // Ensure input field and send button are enabled initially
    inputField.disabled = false;
    sendButton.disabled = false;
    updateSendButtonState(); // Initial check for send button state
});
