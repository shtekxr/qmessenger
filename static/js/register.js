document.getElementById('registrationForm').addEventListener('submit',
    async function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    // Добавляем недостающие поля
    data.is_active = true;
    data.is_superuser = false;
    data.is_verified = false;
    data.chat_ids = [];

    const response = await fetch('/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        alert('Регистрация прошла успешно!');
    } else {
        alert('Ошибка регистрации.');
    }
});