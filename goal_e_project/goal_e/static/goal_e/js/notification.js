// Notification message handling function

function hideNotification(secondsDelay) {
    const notif = document.querySelector('.message');

    setTimeout(() => {
        notif.classList.add('hide');
    }, secondsDelay * 1000);
}