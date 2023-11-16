/* Utility functions for user interface */

function showElement(id) {
    const ele = document.getElementById(id);
    ele.classList.remove('hide');
}

function hideElement(id) {
    const ele = document.getElementById(id);
    ele.classList.add('hide');
}