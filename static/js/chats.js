// Получаем модальное окно
var modal = document.getElementById('myModal');

// Получаем кнопку, которая открывает модальное окно
var btn = document.getElementById('new_chat');

// Получаем элемент <span>, который закрывает модальное окно
var span = document.getElementsByClassName('close')[0];

// Когда пользователь кликает на кнопку, открываем модальное окно
btn.onclick = function() {
  modal.style.display = 'block';
}

// Когда пользователь кликает на <span> (x), закрываем модальное окно
span.onclick = function() {
  modal.style.display = 'none';
}

// Когда пользователь кликает в любом месте за пределами модального окна, закрываем его
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = 'none';
  }
}