document.getElementById('login-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);


    const response = await fetch('/auth/jwt/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString()
    });

    if (response.status === 204) {
        window.location.href = '/chats';
    } else {
        alert('Login failed!');
    }
});


document.addEventListener("DOMContentLoaded", function() {
    const cookieConsent = document.getElementById('cookieConsent');
    const acceptCookies = document.getElementById('acceptCookies');
    const declineCookies = document.getElementById('declineCookies');

    if (!getCookie('cookieConsent')) {
        cookieConsent.classList.add('show');
    }

    acceptCookies.addEventListener('click', function() {
        setCookie('cookieConsent', 'true', 365);
        cookieConsent.classList.remove('show');
    });

    declineCookies.addEventListener('click', function () {
        setCookie('cookieConsent', 'true', 365);
        cookieConsent.classList.remove('show');
    });

    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "expires=" + date.toUTCString();
        document.cookie = name + "=" + value + ";" + expires + ";path=/";
    }

    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }
});

// if (‘serviceWorker’ in navigator) {
//  window.addEventListener(‘load’, function() {
//    navigator.serviceWorker.register(‘/sw.js’).then(
//      function(registration) {
//        // Registration was successful
//        console.log(‘ServiceWorker registration successful with scope: ‘, registration.scope); },
//      function(err) {
//        // registration failed :(
//        console.log(‘ServiceWorker registration failed: ‘, err);
//      });
//  });
// }
