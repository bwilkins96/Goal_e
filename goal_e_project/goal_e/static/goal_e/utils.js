/* Utility functions for user interface */

const serverURL = 'http://localhost:8000';

function showElement(id) {
    const ele = document.getElementById(id);
    ele.classList.remove('hide');
}

function hideElement(id) {
    const ele = document.getElementById(id);
    ele.classList.add('hide');
}

function showElementOverlay(id) {
    showElement('overlay');
    showElement(id);
}

function hideElementOverlay(id) {
    hideElement('overlay');
    hideElement(id);
}

function csrfVal() {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return csrfToken.value;
}

async function completeGoalReq(id) {
    const reqOptions = {
        method: 'POST',

        headers: {
            'X-CSRFToken': csrfVal()
        }
    };
    
    const response = await fetch(serverURL + '/goals/' + id + '/complete', reqOptions);
    const jsonData = await response.json();
    
    return jsonData;
}

async function markGoalComplete(id) {
    responseData = await completeGoalReq(id);
    
    const goalCard = document.getElementById(id);
    const completeBtn = goalCard.querySelector('.completeBtn');
    const progBar = goalCard.querySelector('.progBar .bar');

    completeBtn.classList.add('completedMsg');
    completeBtn.innerText = 'Completed on November 2, 2023!';
    progBar.style.width = '100%';
}