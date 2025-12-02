const monthYearElement = document.getElementById('monthYear');
const datesElement = document.getElementById('dates');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

// add events here, date and then whaever and order etc

const events = {
    "2025-12-01": [
      "9:00 AM: Pickleball Open Play",
      "4:00 PM: Youth Basketball Practice"
    ],
    "2025-12-02": [
      "7:30 AM: Morning Bootcamp",
      "6:00 PM: Wine Tasting"
    ],
    "2025-12-03": [
      "10:00 AM: Yoga Session",
      "5:00 PM: Teen Lounge Hangout"
    ],
    "2025-12-04": [
      "3:00 PM: Kids Art Class",
      "7:00 PM: Game Night"
    ],
    "2025-12-05": [
      "6:00 PM: Holiday Mixer",
      "8:00 PM: Movie Night"
    ],
    "2025-12-06": [
      "9:00 AM: Youth Soccer Game",
      "2:00 PM: Community Garden Workday"
    ],
    "2025-12-07": [
      "8:00 AM: Trail Clean-Up",
      "11:00 AM: Brunch Club Meet-Up"
    ],
    "2025-12-08": [
      "9:00 AM: Basketball Open Play",
      "4:00 PM: Homework Help"
    ],
    "2025-12-09": [
      "7:00 AM: Spin Class",
      "6:30 PM: Young Professionals Meet-Up"
    ],
    "2025-12-10": [
      "10:00 AM: Meditation Session",
      "5:30 PM: Pickleball Ladder Match"
    ],
    "2025-12-11": [
      "3:00 PM: Kid’s Playroom Free Time",
      "7:00 PM: Community Volunteer Night"
    ],
    "2025-12-12": [
      "9:00 AM: Baking Session",
      "6:00 PM: Craft Market Preview Night"
    ],
    "2025-12-13": [
      "10:00 AM: Fall/Winter Craft Market",
      "2:00 PM: Youth Tennis Clinic"
    ],
    "2025-12-14": [
      "9:00 AM: Open Swim",
      "4:00 PM: Movie Night"
    ],
    "2025-12-15": [
      "7:30 AM: Morning Bootcamp",
      "5:00 PM: Community Garden Prep"
    ],
    "2025-12-16": [
      "10:00 AM: Coffee Meetup",
      "6:00 PM: Pickleball Scrimmages"
    ],
    "2025-12-17": [
      "11:00 AM: Yoga Flow",
      "4:30 PM: Youth Basketball Game"
    ],
    "2025-12-18": [
      "9:00 AM: Spin Class",
      "7:00 PM: Winter Formal"
    ],
    "2025-12-19": [
      "8:00 AM: Weight Room Orientation",
      "6:30 PM: Wine Tasting"
    ],
    "2025-12-20": [
      "10:00 AM: Kids Sports Day",
      "2:00 PM: Kayaking Trip (Weather Permitting)"
    ],
    "2025-12-21": [
      "9:00 AM: Pickleball Round Robin",
      "4:00 PM: Holiday Craft Workshop"
    ],
    "2025-12-22": [
      "8:00 AM: Cardio Circuit",
      "5:00 PM: Teen Lounge Holiday Social"
    ],
    "2025-12-23": [
      "10:00 AM: Community Kitchen Baking Day",
      "6:00 PM: Family Game Night"
    ],
    "2025-12-24": [
      "Whole Day: Open Gym",
      "4:00 PM: Winter Storytime for Kids"
    ],
    "2025-12-25": [
      "Whole Day: Building Closed for Holiday",
    ],
    "2025-12-26": [
      "9:00 AM: Yoga Session",
      "3:00 PM: Indoor Soccer Pickup"
    ],
    "2025-12-27": [
      "10:00 AM: Basketball Tournament",
      "5:00 PM: Movie Night"
    ],
    "2025-12-28": [
      "7:30 AM: Morning Bootcamp",
      "11:00 AM: Brunch Club Meet-Up"
    ],
    "2025-12-29": [
      "9:00 AM: Pickleball Open Play",
      "4:00 PM: Youth Tennis Lessons"
    ],
    "2025-12-30": [
      "8:00 AM: Weight Room Training Block",
      "6:00 PM: Holiday Mixer"
    ],
    "2025-12-31": [
      "10:00 AM: Meditation and Reflection Session",
      "7:00 PM: New Year's Eve Social"
    ],
    
    "2026-01-01": [
    "Whole Day: Open Gym",
    "3:00 PM: New Year’s Recovery Yoga"
    ],
  "2026-01-02": [
    "9:00 AM: Pickleball Open Play",
    "5:00 PM: Teen Lounge Hangout"
    ],
  "2026-01-03": [
    "8:00 AM: Morning Bootcamp",
    "2:00 PM: Youth Basketball Game"
    ],
  "2026-01-04": [
    "10:00 AM: Community Garden Meetup",
    "4:00 PM: Movie Night"
    ],
  "2026-01-05": [
    "9:00 AM: Basketball Open Play",
    "6:00 PM: Winter Craft Workshop"
    ],
  "2026-01-06": [
    "7:00 AM: Spin Class",
    "6:30 PM: Game Night"
    ],
  "2026-01-07": [
    "10:00 AM: Yoga Session",
    "5:00 PM: Youth Art Hour"
    ],
  "2026-01-08": [
    "3:00 PM: Kids Playroom Time",
    "7:00 PM: Wine Tasting"
    ],
  "2026-01-09": [
    "9:00 AM: Baking Session",
    "6:00 PM: Pickleball Ladder Match"
    ],
  "2026-01-10": [
    "10:00 AM: Youth Soccer Game",
    "2:00 PM: Kayaking Trip (Weather Permitting)"
    ],
  "2026-01-11": [
    "8:00 AM: Trail Clean-Up",
    "11:00 AM: Brunch Club Meet-Up"
    ],
  "2026-01-12": [
    "9:00 AM: Weight Room Training Block",
    "4:00 PM: Homework Help"
    ],
  "2026-01-13": [
    "10:00 AM: Coffee Meetup",
    "6:00 PM: Young Professionals Social"
    ],
  "2026-01-14": [
    "11:00 AM: Meditation Session",
    "4:30 PM: Youth Tennis Clinic"
    ],
  "2026-01-15": [
    "9:00 AM: Spin Class",
    "6:00 PM: Game Night"
    ],
  "2026-01-16": [
    "8:00 AM: Weight Room Orientation",
    "6:30 PM: Wine Tasting"
    ],
  "2026-01-17": [
    "10:00 AM: Community Garden Planning",
    "3:00 PM: Indoor Pickleball Games"
    ],
  "2026-01-18": [
    "9:00 AM: Open Swim",
    "4:00 PM: Family Movie Night"
    ],
  "2026-01-19": [
    "7:30 AM: Morning Bootcamp",
    "5:00 PM: Teen Lounge Gathering"
    ],
  "2026-01-20": [
    "9:00 AM: Cardio Studio Circuit",
    "6:00 PM: Volunteer Night"
    ],
  "2026-01-21": [
    "10:00 AM: Community Kitchen Cooking Day",
    "6:00 PM: Pickleball Scrimmages"
    ],
  "2026-01-22": [
    "3:00 PM: Kid’s Art Class",
    "7:00 PM: Winter Social Night"
    ],
  "2026-01-23": [
    "11:00 AM: Yoga Flow",
    "4:00 PM: Youth Basketball Practice"
    ],
  "2026-01-24": [
    "10:00 AM: Basketball Tournament",
    "5:00 PM: Movie Night"
    ],
  "2026-01-25": [
    "9:00 AM: Pickleball Open Play",
    "11:00 AM: Brunch Club Meet-Up"
    ],
  "2026-01-26": [
    "9:00 AM: Baking Session",
    "4:00 PM: Kids Playroom Free Time"
    ],
  "2026-01-27": [
    "10:00 AM: Meditation Space Open Hours",
    "6:30 PM: Game Night"
    ],
  "2026-01-28": [
    "7:00 AM: Spin Class",
    "4:00 PM: Youth Tennis Lessons"
    ],
  "2026-01-29": [
    "9:00 AM: Basketball Open Play",
    "6:00 PM: Winter Mixer"
    ],
  "2026-01-30": [
    "8:00 AM: Weight Room Training Block",
    "6:00 PM: Community Volunteer Night"
    ],
  "2026-01-31": [
    "10:00 AM: Yoga and Stretch Session",
    "7:00 PM: Winter Community Dinner"
    ]
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
