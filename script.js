function sendMessage() {
    const messageInput = document.getElementById('message');
    const message = messageInput.value;
    
    if (message.trim() !== '') {
        // Append the user's message
        appendMessage('user', message);

        // Clear the input field
        messageInput.value = '';

        //send the msg to flask backend
        fetch('http://127.0.0.1:5000/chat',{
            method: 'POST',
            headers: {
                'Content-Type' : 'application/json'
            },
            body:JSON.stringify({message:message})
        })
        .then(Response =>Response.json())
        .then(data => {

            console.log('Success:', data); // Log the entire data object
            appendMessage('bot', data.response);  // Access 'response' in the returned data
            //append bot response
            
        })
        .catch(error => {
            console.error('Error:',error);
            appendMessage('bot','There was an error processing your message.')
        });

        
    }
}

function appendMessage(sender, text) {
    const chatHistory = document.getElementById('chat-history');
    
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    
    const messageText = document.createElement('p');
    messageText.textContent = text;
    
    messageDiv.appendChild(messageText);
    chatHistory.appendChild(messageDiv);

    // Scroll to the bottom of the chat history
    chatHistory.scrollTop = chatHistory.scrollHeight;
}
