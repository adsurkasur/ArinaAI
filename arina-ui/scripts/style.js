document.addEventListener("DOMContentLoaded", function () {
    const toggleSwitch = document.getElementById("themeToggle");
    const body = document.body;

    function setTheme(isDark) {
        if (isDark) {
            body.classList.add("dark-mode");
            body.classList.remove("light-mode");
        } else {
            body.classList.add("light-mode");
            body.classList.remove("dark-mode");
        }
    }

    toggleSwitch.addEventListener("change", function () {
        setTheme(this.checked);
    });

    setTheme(toggleSwitch.checked);
});
