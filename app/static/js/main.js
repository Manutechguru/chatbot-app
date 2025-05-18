const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const clearChatBtn = document.getElementById('clear-chat');
const suggestionButtons = document.querySelectorAll('.prompt-btn');
const fileForm = document.getElementById('upload-form');
const fileInput = document.getElementById('file-input');

// Reusable function to send a message
async function sendMessage(message) {
  if (!message) return;

  // Display user's message
  const userMessageDiv = document.createElement('div');
  userMessageDiv.className = 'user-message';
  userMessageDiv.textContent = message;
  chatBox.appendChild(userMessageDiv);

  userInput.value = '';
  chatBox.scrollTop = chatBox.scrollHeight;

  // Show typing animation
  const botMessageDiv = document.createElement('div');
  botMessageDiv.className = 'bot-message';
  botMessageDiv.innerHTML = `<div class="typing-dots"><span>.</span><span>.</span><span>.</span></div>`;
  chatBox.appendChild(botMessageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    const reply = data.response || "🤖 Sorry, no response.";

    // Remove typing and show AI reply
    chatBox.removeChild(botMessageDiv);
    const realBotMessage = document.createElement('div');
    realBotMessage.className = 'bot-message';
    realBotMessage.innerHTML = reply;
    chatBox.appendChild(realBotMessage);
    chatBox.scrollTop = chatBox.scrollHeight;

  } catch (error) {
    console.error('Error:', error);
    botMessageDiv.innerHTML = "⚠️ Error contacting AI.";
  }
}

// Handle normal chat form
chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  await sendMessage(message);
});

// Clear chat
clearChatBtn.addEventListener('click', () => {
  chatBox.innerHTML = '';
});

// Handle prompt suggestions
suggestionButtons.forEach(button => {
  button.addEventListener('click', () => {
    const message = button.textContent.trim();
    sendMessage(message);
  });
});

// Handle file upload form
fileForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const file = fileInput.files[0];
  if (!file) return;

  // Display file name as user message
  const userFileMsg = document.createElement('div');
  userFileMsg.className = 'user-message';
  userFileMsg.textContent = `📎 Uploaded file: ${file.name}`;
  chatBox.appendChild(userFileMsg);
  chatBox.scrollTop = chatBox.scrollHeight;

  // Show typing animation
  const botMessageDiv = document.createElement('div');
  botMessageDiv.className = 'bot-message';
  botMessageDiv.innerHTML = `<div class="typing-dots"><span>.</span><span>.</span><span>.</span></div>`;
  chatBox.appendChild(botMessageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/upload', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    const reply = data.response || "🤖 Could not process the file.";

    // Remove typing and display AI's file-based reply
    chatBox.removeChild(botMessageDiv);
    const botReply = document.createElement('div');
    botReply.className = 'bot-message';
    botReply.innerHTML = reply;
    chatBox.appendChild(botReply);
    chatBox.scrollTop = chatBox.scrollHeight;

  } catch (err) {
    console.error('File upload error:', err);
    botMessageDiv.innerHTML = "⚠️ File upload failed.";
  }

  // Reset form
  fileInput.value = '';
});


