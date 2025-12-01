const monthYearElement = document.getElementById('monthYear');
const datesElement = document.getElementById('dates');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

// add events here, date and then whaever and order etc

const events = {
  "2025-11-29": ["9:00 AM: Basketball game", "11:00 AM: Open Gym"],
  "2025-11-30": ["Whole Day: Birthday Reservation"]
};

let currentDate = new Date();

const updateCalendar = () => {
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    const totalDays = lastDay.getDate();
    const firstDayIndex = firstDay.getDay();
    const lastDayIndex = lastDay.getDay();
    
    const monthYearString = currentDate.toLocaleString('default', { month: 'long', year: 'numeric' });
    monthYearElement.textContent = monthYearString;

    let datesHTML = '';

    
    const prevMonthLastDay = new Date(currentYear, currentMonth, 0).getDate();
    for (let i = firstDayIndex; i > 0; i--) {
        datesHTML += `<div class="date inactive">${prevMonthLastDay - i + 1}</div>`;
    }

    
    for (let i = 1; i <= totalDays; i++) {
        const date = new Date(currentYear, currentMonth, i);
        const dateKey = date.toISOString().split('T')[0];
        const activeClass = date.toDateString() === new Date().toDateString() ? 'active' : '';
        const eventClass = events[dateKey] ? 'has-event' : '';
        datesHTML += `<div class="date ${activeClass} ${eventClass}" data-date="${dateKey}">${i}</div>`;
    }

    
    for (let i = 1; i < 7 - lastDayIndex; i++) {
        datesHTML += `<div class="date inactive">${i}</div>`;
    }


    datesElement.innerHTML = datesHTML;
};

prevBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar();
});

nextBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
});

datesElement.addEventListener('click', (e) =>{
    if (e.target.classList.contains('date')) {
        const dateKey = e.target.dataset.date;
        const eventList = document.getElementById('eventList');
        
        if (events[dateKey]){
            eventList.innerHTML = events[dateKey].map(ev => `<p>${ev}</p>`).join('');
        } else {
            eventList.innerHTML = "<p>No events for this day.</p>";
        }
    }
});

updateCalendar();
