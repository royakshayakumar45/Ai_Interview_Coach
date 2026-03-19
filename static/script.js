function startApp() {
    alert("🚀 Welcome to AI Interview Coach!");
}

// Smooth scroll effect
document.querySelectorAll("li").forEach(item => {
    item.addEventListener("click", () => {
        window.scrollTo({ top: 500, behavior: "smooth" });
    });
});