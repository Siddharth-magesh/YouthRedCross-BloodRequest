document.getElementById("admin-button").addEventListener("click", function () {
    const dropdown = document.getElementById("admin-dropdown");
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
});

// For displaying date and time
function updateDateTime() {
    const dateTimeElement = document.getElementById("date-time");
    const now = new Date();
    dateTimeElement.textContent = now.toLocaleString();
}

setInterval(updateDateTime, 1000);
