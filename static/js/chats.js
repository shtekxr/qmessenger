const modal = document.querySelector('#modal');
const btn = document.querySelector('#new_chat');
const close = document.querySelector('.close');
const create_btn = document.getElementById('create-chat-btn')

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

create_btn.onclick = createChat

async function createChat(event) {
    event.preventDefault();
    const new_chat_name = document.getElementById('new_chat_name').value;
    try {
        const response = await fetch(`/chats/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(new_chat_name),
        });


        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log(await response)
        const result = await response.json();

        alert(result.message);

    } catch (error) {
        console.error('Error:', error);
            alert('An error occurred while creating the chat.');
    }
}