/* Calendar related functions */

// Redirect calendar on input change 
function getMonthYear(inputVal) {
    let [year, month] = inputVal.split('-');
    month = Number(month);

    return [month, year]
}

function handleMonthChange(url) {
    const monthVal = document.getElementById('monthInput').value;            
    const [month, year] = getMonthYear(monthVal); 

    if (month && year) {
        window.location = `${url}/${month}/${year}`; 
    } else {
        window.location = url
    }
}

// Add today class for current day
function applyTodayClass(todayId) {
    todayEle = document.getElementById(todayId);
    todayEle.classList.add('today');
}