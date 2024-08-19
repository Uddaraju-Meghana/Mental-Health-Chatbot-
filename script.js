function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') {
        return;
    }

    // Display user message
    var messagesDiv = document.getElementById('messages');
    var userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('user-message');
    userMessageDiv.textContent = userInput;
    messagesDiv.appendChild(userMessageDiv);

    // Clear input field
    document.getElementById('user-input').value = '';

    // Send message to server
    fetch(`/get?msg=${encodeURIComponent(userInput)}`)
        .then(response => response.text())
        .then(data => {
            var botMessageDiv = document.createElement('div');
            botMessageDiv.classList.add('bot-message');
            botMessageDiv.textContent = data;
            messagesDiv.appendChild(botMessageDiv);
        });

    // Scroll to the bottom
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
