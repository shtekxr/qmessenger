const url = window.location.href;
const chatID = url.match(/\/chats\/(\d+)/)[1];
const ws = new WebSocket(`wss://rizem.ru/chats/${chatID}/ws`);
// const ws = new WebSocket(`ws://localhost/chats/${chatID}/ws`);

function scrollToBottom() {
    const messages = document.getElementById('messages');
    messages.scrollTop = messages.scrollHeight;
}

ws.onmessage = function(event) {
    const messages = document.getElementById('messages');
    const messageData = JSON.parse(event.data);

    const messageContainer = document.createElement('div')
    const messageWrapper = document.createElement('div');
    const usernameElement = document.createElement('div');
    const messageElement = document.createElement('div');
    const timeElement = document.createElement('div');

    usernameElement.textContent = messageData.username;
    messageElement.textContent = messageData.message;
    timeElement.textContent = messageData.time;

    messageContainer.classList.add('message-container')
    usernameElement.classList.add('username');
    messageWrapper.classList.add('received-message');
    timeElement.classList.add('time');

    messageWrapper.appendChild(usernameElement);
    messageWrapper.appendChild(messageElement);
    messageWrapper.appendChild(timeElement);
    messageContainer.appendChild(messageWrapper)
    messages.appendChild(messageContainer);

    scrollToBottom();

    setTimeout(function() {
        scrollToBottom();
        console.log(123)
    }, 2000);

};
function sendMessage(event) {
    const input = document.getElementById('messageText');
    const message = document.createElement('div');
    const content = document.createTextNode(input.value);
    const time = new Date().toLocaleTimeString();

    const timeElement = document.createElement('span');
    timeElement.textContent = ` (${time})`;

    // message.appendChild(content);
    // message.appendChild(timeElement);
    // message.classList.add('sent-message');

    const messages = document.getElementById('messages');
    messages.appendChild(message);


    ws.send(input.value);
    input.value = '';
    event.preventDefault();
    messages.scrollTop = messages.scrollHeight;
}

const modal = document.querySelector('#modal');
const settings = document.querySelector('#top-settings');
const close = document.querySelector('.close');
const chat_user = document.querySelector('.chat-user')
const invite = document.getElementById('invite')


settings.onclick = function () {
    modal.style.display = 'block';
    const response = fetch(`${chatID}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
};

close.onclick = function () {
  modal.style.display = 'none';
};

invite.onclick = inviteUser;

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = 'none';
  }
};


document.getElementById('top-back').onclick = function () {
    location.href = '/chats'
}






async function inviteUser(event) {
    event.preventDefault();
    const username = document.getElementById('invite_username').value;
    try {
        const response = await fetch(`${chatID}/${username}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        alert(result.message);
        console.log(result.message);
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}



async function kickUser(username) {
    if (confirm('Are you sure you want to kick '+username+'?')) {
        try {
            const response = await fetch(`${chatID}/kick/${username}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                // Для PATCH запросов обычно не требуется тело, но можно передать пустой объект {}
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const result = await response.json();
            alert(result.message); // Выводим сообщение от сервера
            console.log(result); // Логируем результат в консоль для отладки
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while kicking the user.'); // В случае ошибки выводим сообщение пользователю
        }
    }
}


window.onload = function() {
    ws.onopen = function() {
        scrollToBottom();
    };
}