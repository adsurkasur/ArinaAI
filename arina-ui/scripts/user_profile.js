document.addEventListener("DOMContentLoaded", () => {
    const userName = "Jane Doe"; // Replace with the actual user's name
    const greetingText = document.querySelector(".greeting-text");
    greetingText.textContent = `Hello, ${userName}!`;
});