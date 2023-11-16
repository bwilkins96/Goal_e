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

// Functions for ui handling of goal completion
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

function setCompletedPopUp(resData) {
    const upperPopUp = document.getElementById('upperPopUp');
    const titleSpan = upperPopUp.querySelector('.popUpTitle');
    const pointsSpan = upperPopUp.querySelector('.popUpPoints');

    titleSpan.innerText = resData['title'];
    pointsSpan.innerText = resData['pointsAdded'];
}

function showCompletedPopUp(resData) {
    setCompletedPopUp(resData);
    showElementOverlay('completedPopUp');
    
    document.body.addEventListener('click', () => {
        hideElementOverlay('completedPopUp');
    }, { once: true });
}

function updateGoalCard(id, resData) {
    const goalCard = document.getElementById(id);
    const completeBtn = goalCard.querySelector('.completeBtn');
    const progBar = goalCard.querySelector('.progBar .bar');
    const progText = goalCard.querySelector('.progBar p');

    completeBtn.classList.add('completedMsg');
    completeBtn.innerText = `Completed on ${resData['dateStr']}!`;
    completeBtn.onclick = null;

    progBar.style.width = '100%';
    progText.innerText = '100%';
}

async function markGoalComplete(id) {
    responseData = await completeGoalReq(id);
    showCompletedPopUp(responseData);
    updateGoalCard(id, responseData);
}