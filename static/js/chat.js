const url = window.location.href;
const chatID = url.match(/\/chats\/(\d+)/)[1];
const ws = new WebSocket(`ws://localhost:8000/chats/${chatID}/ws`);
ws.onmessage = function(event) {
    const messages = document.getElementById('messages');
    const message = document.createElement('div');
    const content = document.createTextNode(event.data);
    message.appendChild(content)
    messages.appendChild(message)
};
function sendMessage(event) {
    const input = document.getElementById("messageText");
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}

const modal = document.querySelector('#modal');
const btn = document.querySelector('#top-invite');
// const close = document.querySelector('.close');
const close = document.querySelector('#close');

btn.onclick = function () {
  modal.style.display = 'block';
};

close.onclick = function () {
  modal.style.display = 'none';

};

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = 'none';
  }
};


document.getElementById('top-back').onclick = function () {
    location.href = '/chats'
}