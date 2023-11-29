/* Functions for the account settings page  */

// Functions for changing the theme
function setThemeInputVal(val) {
    themeInput = document.getElementById('theme');
    themeInput.value = val;
}

function getThemeInputVal() {
    return document.getElementById('theme').value;
}

function changeThemeStyling(currentBtn, currentVal, prevVal) {
    prevBtn = document.getElementById(`themeBtn${prevVal}`);    
    prevBtn.classList.remove('selected');
    currentBtn.classList.add('selected');

    document.body.classList.remove(`theme${prevVal}`);

    if (currentVal > 1) {
        document.body.classList.add(`theme${currentVal}`);
    }
}

function changeTheme(ele, val) {
    const prevVal = getThemeInputVal();
    
    setThemeInputVal(val);
    changeThemeStyling(ele, val, prevVal);
}