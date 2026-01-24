// Main Chat UI logic for the grey chatbox
function initChatbotUI() {
  if (window.__chatbotLoaded) return;
  window.__chatbotLoaded = true;

  var chatRoot = document.getElementById('chatbot');
  if (!chatRoot) return;

  // Hide any duplicate chat UI elements if present
  var blob = document.getElementById('chatbox-blob');
  if (blob) blob.style.display = 'none';
  var popup = document.getElementById('chatbot-popup');
  if (popup) popup.style.display = 'none';

  var messagesEl = document.getElementById('chatMessages');
  var inputEl = document.getElementById('chatInput');
  var submitBtn = document.getElementById('submitButton');

  if (!messagesEl || !inputEl || !submitBtn) return;

  var isSending = false;
  var REQUEST_TIMEOUT_MS = 15000;
  var isLocalHost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  var isFileProtocol = window.location.protocol === 'file:';
  var API_URL = window.MHM_CHATBOT_API_URL
    || (isLocalHost || isFileProtocol
      ? 'http://localhost:5001/api/chat'
      : window.location.origin + '/api/chat');

  function addMessage(text, isUser) {
    var msg = document.createElement('div');
    msg.className = 'chat-message ' + (isUser ? 'user' : 'bot');
    msg.textContent = text;
    messagesEl.appendChild(msg);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function addTyping() {
    var msg = document.createElement('div');
    msg.className = 'chat-message bot typing';
    msg.id = 'chat-typing';
    msg.textContent = 'Typing...';
    messagesEl.appendChild(msg);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function removeTyping() {
    var typing = document.getElementById('chat-typing');
    if (typing) typing.remove();
  }

  function setSending(state) {
    isSending = state;
    submitBtn.disabled = isSending || inputEl.value.trim().length === 0;
  }

  function sendMessage() {
    var message = inputEl.value.trim();
    if (!message || isSending) return;

    setSending(true);
    addMessage(message, true);
    inputEl.value = '';
    setSending(true);
    addTyping();

    var controller = new AbortController();
    var timeoutId = setTimeout(function() { controller.abort(); }, REQUEST_TIMEOUT_MS);

    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: message }),
      signal: controller.signal
    })
      .then(function(response) {
        clearTimeout(timeoutId);
        if (!response.ok) throw new Error('Bad response');
        return response.json();
      })
      .then(function(data) {
        removeTyping();
        if (data && data.status === 'success' && data.response) {
          addMessage(String(data.response), false);
        } else {
          addMessage('I ran into an issue. Please try again.', false);
        }
      })
      .catch(function(error) {
        removeTyping();
        if (error && error.name === 'AbortError') {
          addMessage('The request timed out. Please try again.', false);
        } else {
          addMessage('I cannot connect to the server. Please make sure the backend is running.', false);
        }
      })
      .finally(function() {
        setSending(false);
        inputEl.focus();
      });
  }

  submitBtn.addEventListener('click', sendMessage);
  inputEl.addEventListener('input', function() { setSending(false); });
  inputEl.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendMessage();
    }
  });

  setSending(false);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initChatbotUI);
} else {
  initChatbotUI();
}

// Functions to open/close chatbot (for other UI triggers)
function openChat() {
  document.getElementById("chatbot").classList.add("open");
}

function closeChat() {
  document.getElementById("chatbot").classList.remove("open");
}
