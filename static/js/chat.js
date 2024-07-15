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