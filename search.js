document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("searchInput");
  const events = document.querySelectorAll(".event");
  const noResults = document.getElementById("noResults");

  let activeCategory = "all";

  // Initially hide all events
  events.forEach(event => event.classList.remove("visible"));

  // Function to filter events
  function filterEvents() {
    const searchTerm = searchInput.value.toLowerCase();

    // Hide all events first
    events.forEach(event => event.classList.remove("visible"));

    // Filter events matching search & category
    const matchingEvents = Array.from(events).filter(event => {
      const text = event.innerText.toLowerCase();
      const category = event.dataset.category;
      const matchesSearch = text.includes(searchTerm);
      const matchesCategory = activeCategory === "all" || category === activeCategory;
      return matchesSearch && matchesCategory;
    });

    // Show top 6 matching events
    matchingEvents.slice(0, 6).forEach(event => event.classList.add("visible"));

    // Show "no results" message if nothing matches
    noResults.style.display = matchingEvents.length === 0 ? "block" : "none";
  }

  // Listen for input in search box
  searchInput.addEventListener("input", filterEvents);

  // Optional: category filter buttons (if using)
  document.querySelectorAll("[data-filter]").forEach(button => {
    button.addEventListener("click", () => {
      activeCategory = button.dataset.filter;
      filterEvents();
    });
  });
});
