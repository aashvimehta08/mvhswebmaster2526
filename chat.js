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
  var formEl = document.getElementById('chatInputSection');

  if (!messagesEl || !inputEl || !submitBtn || !formEl) return;

  var chatWindow = document.getElementById('chatWindow');
  if (chatWindow) {
    var controls = document.getElementById('chatControls');
    var closeIcon = document.getElementById('closeIcon');
    var infoToggle = document.getElementById('infoToggle');

    if (!controls) {
      controls = document.createElement('div');
      controls.id = 'chatControls';
      if (chatWindow.firstChild) {
        chatWindow.insertBefore(controls, chatWindow.firstChild);
      } else {
        chatWindow.appendChild(controls);
      }
    }

    if (!infoToggle) {
      infoToggle = document.createElement('button');
      infoToggle.id = 'infoToggle';
      infoToggle.setAttribute('aria-label', 'Show info');
      infoToggle.innerHTML = '<span>?</span>';
      controls.appendChild(infoToggle);
    }

    if (closeIcon && closeIcon.parentNode !== controls) {
      controls.appendChild(closeIcon);
    }

    var infoWidget = document.getElementById('infoWidget');
    if (!infoWidget) {
      infoWidget = document.createElement('div');
      infoWidget.id = 'infoWidget';
      infoWidget.style.display = 'none';
      infoWidget.innerHTML = ''
        + '<h2>How to Prompt the Chatbot</h2>'
        + '<ul>'
        + '<li><b>Find calendar events:</b> <br><span style="opacity:0.9;">"Events on 1/26/2026" or "Show events on January 26"</span></li>'
        + '<li><b>Ask about activities:</b> <br><span style="opacity:0.9;">"Do you have pickleball?" or "Tell me about hiking trails"</span></li>'
        + '<li><b>Find the mission statement:</b> <br><span style="opacity:0.9;">"What is the mission statement?"</span></li>'
        + '<li><b>Origin story:</b> <br><span style="opacity:0.9;">"How did you begin?" or "Where did you start?"</span></li>'
        + '<li><b>Contact info:</b> <br><span style="opacity:0.9;">"What is the phone number?" or "What is your email?"</span></li>'
        + '<li><b>FAQs:</b> <br><span style="opacity:0.9;">"What programs do you offer?" or "How much does it cost?"</span></li>'
        + '<li><b>General tips:</b> <br><span style="opacity:0.9;">Use keywords like "kids", "culinary", "sports", or "outdoor" for best results.</span></li>'
        + '</ul>';
      var chatText = document.getElementById('chatText');
      if (chatText && chatText.nextSibling) {
        chatWindow.insertBefore(infoWidget, chatText.nextSibling);
      } else {
        chatWindow.insertBefore(infoWidget, messagesEl);
      }
    }
    if (infoWidget && infoWidget.innerHTML.trim().length === 0) {
      infoWidget.innerHTML = ''
        + '<h2>How to Prompt the Chatbot</h2>'
        + '<ul>'
        + '<li><b>Find calendar events:</b> <br><span style="opacity:0.9;">"Events on 1/26/2026" or "Show events on January 26"</span></li>'
        + '<li><b>Ask about activities:</b> <br><span style="opacity:0.9;">"Do you have pickleball?" or "Tell me about hiking trails"</span></li>'
        + '<li><b>Find the mission statement:</b> <br><span style="opacity:0.9;">"What is the mission statement?"</span></li>'
        + '<li><b>Origin story:</b> <br><span style="opacity:0.9;">"How did you begin?" or "Where did you start?"</span></li>'
        + '<li><b>Contact info:</b> <br><span style="opacity:0.9;">"What is the phone number?" or "What is your email?"</span></li>'
        + '<li><b>FAQs:</b> <br><span style="opacity:0.9;">"What programs do you offer?" or "How much does it cost?"</span></li>'
        + '<li><b>General tips:</b> <br><span style="opacity:0.9;">Use keywords like "kids", "culinary", "sports", or "outdoor" for best results.</span></li>'
        + '</ul>';
    }

    var infoClose = document.getElementById('infoClose');
    if (infoToggle && infoWidget) {
      infoToggle.addEventListener('click', function() {
        infoWidget.style.display = infoWidget.style.display === 'none' ? 'block' : 'none';
      });
    }
    if (infoClose && infoWidget) {
      infoClose.addEventListener('click', function() {
        infoWidget.style.display = 'none';
      });
    }
  }

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

  formEl.addEventListener('submit', function(e) {
    e.preventDefault();
    sendMessage();
  });
  submitBtn.addEventListener('click', sendMessage);
  inputEl.addEventListener('input', function() { setSending(false); });
  inputEl.addEventListener('keydown', function(e) {
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
