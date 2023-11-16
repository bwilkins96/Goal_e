/* Utility functions for user interface */

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