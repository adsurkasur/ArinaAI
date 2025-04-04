document.addEventListener("DOMContentLoaded", function () {
    const greetingElement = document.getElementById("greeting-text");
    const greetingText = "Hello! How can Arina help?";
    let index = 0;

    function type() {
        if (index < greetingText.length) {
            greetingElement.textContent = greetingText.substring(0, index + 1);
            index++;
            setTimeout(type, 100);
        }
    }

    type();
});
