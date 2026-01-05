
const filterDropdown = document.getElementById('filterDropdown');

// Set dropdown value from localStorage on page load
window.onload = function() {
    const savedFilter = localStorage.getItem('selectedFilter');
    if (savedFilter) {
    filterDropdown.value = savedFilter;
    }
};

// Save selected value and navigate
filterDropdown.addEventListener('change', function() {
    localStorage.setItem('selectedFilter', this.value);
    window.location.href = this.value;
});