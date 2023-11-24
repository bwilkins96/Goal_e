// Redirect calendar on input change 

function getMonthYear(inputVal) {
    let [year, month] = inputVal.split('-');
    month = Number(month);

    return [month, year]
}

function handleMonthChange(url) {
    const monthVal = document.getElementById('monthInput').value;            
    const [month, year] = getMonthYear(monthVal); 
    console.log(url);
    window.location = `${url}/${month}/${year}`; 
}