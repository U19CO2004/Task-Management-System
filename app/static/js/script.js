// static/js/script.js

// Wait until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Optional: Add a highlight effect on rows when hovered
  const rows = document.querySelectorAll("tbody tr");

  rows.forEach(row => {
    row.addEventListener("mouseenter", () => {
      row.style.backgroundColor = "#f9f9f9";
    });

    row.addEventListener("mouseleave", () => {
      row.style.backgroundColor = "";
    });
  });

  // Optional: Auto-hide flash messages after 3 seconds
  const flashMessages = document.querySelectorAll(".flash");
  flashMessages.forEach(flash => {
    setTimeout(() => {
      flash.style.display = "none";
    }, 3000); // 3 seconds
  });
});
