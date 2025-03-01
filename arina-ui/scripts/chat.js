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

    // Extend input field as user types
    inputField.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + "px";
    });

    // Send message when the button is clicked
    sendButton.addEventListener("click", function () {
        sendButton.disabled = true; // Disable immediately to prevent spamming
        sendMessage();
    });

    // Allow sending messages with Enter key, prevent form submission
    inputField.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !sendButton.disabled) {
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
        messageBubble.classList.add("message", sender);

        if (sender !== "error" && sender !== "user") {
            const profileContainer = document.createElement("div");
            profileContainer.classList.add("profile-container");

            const profilePic = document.createElement("img");
            profilePic.classList.add("profile-pic");
            profilePic.src = "../images/arina.jpg";

            const profileName = document.createElement("span");
            profileName.classList.add("profile-name");
            profileName.textContent = "Arina";

            profileContainer.appendChild(profilePic);
            profileContainer.appendChild(profileName);
            messageBubble.appendChild(profileContainer);
        }

        const messageText = document.createElement("span");
        messageText.textContent = text;
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
            inputField.disabled = false;  // Re-enable input field
            updateSendButtonState();      // Ensure button state updates
        }
    }

    // Ensure input field and send button are enabled initially
    inputField.disabled = false;
    sendButton.disabled = false;
    updateSendButtonState(); // Initial check for send button state
});
