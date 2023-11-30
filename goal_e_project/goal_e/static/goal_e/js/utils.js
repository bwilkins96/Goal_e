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

function updatePointsDisplay(resData) {
    const pointsDisplay = document.getElementById('pointsDisplay');
    pointsDisplay.innerText = `${resData['newPointsTotal']} points`;
}

async function markGoalComplete(id) {
    responseData = await completeGoalReq(id);
    showCompletedPopUp(responseData);
    updateGoalCard(id, responseData);
    updatePointsDisplay(responseData);
}

// Signup / account settings form validation
function clearMessage(msgId) {
    message = document.getElementById(msgId);
    
    if (message) {
        message.remove();
    }
}

function handleNonMatchingPasswords(msgId) {
    const message = document.createElement('p');
    message.id = msgId;
    message.innerText = 'Passwords do not match';

    document.body.appendChild(message);
}

function validatePasswords(e, msgId) {
    clearMessage(msgId);

    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    passwordsFilled = Boolean(password || confirmPassword);

    if (passwordsFilled && (password !== confirmPassword)) {
        e.preventDefault();
        handleNonMatchingPasswords(msgId);
    }
}

function removeAvailableInfo() {
    const usernameInput = document.getElementById('username');
    usernameInput.classList.remove('available');
    usernameInput.classList.remove('unavailable');

    const usernameLabel = document.querySelector('label[for="username"]');
    const availableSpan = document.querySelector('label[for="username"] span');

    if (availableSpan) {
        availableSpan.remove();
    }
}

async function checkUsernameAvailable() {
    const usernameInput = document.getElementById('username');
    const username = usernameInput.value;
    if (!username) {
        return removeAvailableInfo();
    }

    const response = await fetch(serverURL + '/usernameAvailable/' + username);
    const jsonData = await response.json();
    const available = jsonData.available;

    const usernameLabel = document.querySelector('label[for="username"]');
    
    if ((available == true) || (available == 'current username')) {
        usernameInput.classList.add('available');
        usernameLabel.innerHTML = 'Username <span>(Available)</span>';
    } else if (available == 'invalid username') {
        usernameInput.classList.add('unavailable');
        usernameLabel.innerHTML = 'Username <span>(Invalid)</span>';
    } else {
        usernameInput.classList.add('unavailable');
        usernameLabel.innerHTML = 'Username <span>(Not Available)</span>';
    }
}