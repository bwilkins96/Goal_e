/* Functions for add/edit goal forms */

// Functions for changing the progress bar/value
function changeProgBar() {
    const progBar = document.getElementById('progressBar');
    const progInput = document.getElementById('progress');
    progBar.value = progInput.value;
}

function changeProgInput() {
    const progBar = document.getElementById('progressBar');
    const progInput = document.getElementById('progress');
    progInput.value = progBar.value;
}

// Functions for changing the priority
function removePriorityStyles(prev, formEle) {
    const current = document.querySelector('.selected');
    current.classList.remove('selected');

    if (prev == 1) {
        formEle.classList.remove('Low');
    } else if (prev == 2) {
        formEle.classList.remove('Medium');
    } else {
        formEle.classList.remove('High');
    }
}

function addPriorityStyles(val, formEle) {
    if (val == 1) {
        const lowBtn = document.getElementById('lowBtn');
        lowBtn.classList.add('selected');

        formEle.classList.add('Low');
    } else if (val == 2) {
        const medBtn = document.getElementById('medBtn');
        medBtn.classList.add('selected');

        formEle.classList.add('Medium');
    } else {
        const highBtn = document.getElementById('highBtn');
        highBtn.classList.add('selected');

        formEle.classList.add('High');
    }
}

function setPriority(val) {
    const priorityInput = document.getElementById('priority');
    const prevVal = priorityInput.value;
    const formEle = document.getElementById('goalForm');
    
    priorityInput.value = val;
    removePriorityStyles(prevVal, formEle);
    addPriorityStyles(val, formEle);
}