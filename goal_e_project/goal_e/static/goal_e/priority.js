// Functions for changing the priority on a goal form

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