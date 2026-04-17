// Main Chat UI logic for the grey chatbox - Enhanced Version
// Features: Better error handling, timestamps, message caching, analytics, accessibility improvements

// Configuration constants
var CHATBOT_CONFIG = {
  REQUEST_TIMEOUT_MS: 25000,
  MAX_RETRIES: 3,
  RETRY_BACKOFF_MS: 1000,
  STORAGE_KEY: 'chatbot_draft',
  HISTORY_KEY: 'chatbot_history',
  ANALYTICS_KEY: 'chatbot_analytics'
};

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

  // Message tracking and analytics
  var messageHistory = [];
  var questionFrequency = {};

  // Restore draft message from localStorage
  var draftMessage = localStorage.getItem(CHATBOT_CONFIG.STORAGE_KEY);
  if (draftMessage) {
    inputEl.value = draftMessage;
  }

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

    if (!controls) return;

    if (!infoToggle) {
      infoToggle = document.createElement('button');
      infoToggle.id = 'infoToggle';
      infoToggle.setAttribute('aria-label', 'Show chatbot help and prompting tips');
      infoToggle.title = 'Chatbot Help';
      infoToggle.innerHTML = '<span>?</span>';
      controls.appendChild(infoToggle);
    }
    infoToggle.setAttribute('data-tip', 'Help');

    var clearHistoryBtn = document.getElementById('clearHistoryBtn');
    if (clearHistoryBtn) {
      clearHistoryBtn.style.display = 'none';
    }

    if (closeIcon && closeIcon.parentNode !== controls) {
      controls.appendChild(closeIcon);
    }
    if (closeIcon) {
      closeIcon.setAttribute('title', 'Close Chat');
      closeIcon.setAttribute('aria-label', 'Close Chat');
      closeIcon.setAttribute('data-tip', 'Close');
      closeIcon.setAttribute('tabindex', '0');
      closeIcon.setAttribute('role', 'button');
      closeIcon.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          closeChat();
        }
      });
    }

    var helpContentHtml = ''
      + '<div class="info-widget-header">'
      + '<div class="info-widget-heading">'
      + '<h2>How to Prompt the Chatbot</h2>'
      + '</div>'
      + '<button id="infoClose" aria-label="Close help" title="Close">✕</button>'
      + '</div>'
      + '<ul class="tip-grid">'
      + '<li class="tip-card"><span class="tip-label">Find calendar events:</span><span class="tip-example">"Events on 1/26/2026" or "Show events on January 26"</span></li>'
      + '<li class="tip-card"><span class="tip-label">Ask about activities:</span><span class="tip-example">"Do you have pickleball?" or "Tell me about hiking trails"</span></li>'
      + '<li class="tip-card"><span class="tip-label">Find the mission statement:</span><span class="tip-example">"What is the mission statement?"</span></li>'
      + '</ul>';

    var infoWidget = document.getElementById('infoWidget');
    if (!infoWidget) {
      infoWidget = document.createElement('div');
      infoWidget.id = 'infoWidget';
      infoWidget.className = 'info-widget-enhanced';
      infoWidget.style.display = 'none';
      infoWidget.setAttribute('role', 'region');
      infoWidget.setAttribute('aria-label', 'Chatbot help information');
      infoWidget.innerHTML = helpContentHtml;
      var chatText = document.getElementById('chatText');
      if (chatText && chatText.nextSibling) {
        chatWindow.insertBefore(infoWidget, chatText.nextSibling);
      } else {
        chatWindow.insertBefore(infoWidget, messagesEl);
      }
    } else if (!infoWidget.innerHTML || !infoWidget.innerHTML.trim()) {
      infoWidget.innerHTML = helpContentHtml;
      infoWidget.setAttribute('role', 'region');
      infoWidget.setAttribute('aria-label', 'Chatbot help information');
    }

    var infoClose = document.getElementById('infoClose');
    if (infoToggle && infoWidget) {
      infoToggle.addEventListener('click', function() {
        var isHidden = infoWidget.style.display === 'none';
        infoWidget.style.display = isHidden ? 'block' : 'none';
        infoToggle.setAttribute('aria-expanded', isHidden);
      });
    }
    if (infoClose && infoWidget) {
      infoClose.addEventListener('click', function() {
        infoWidget.style.display = 'none';
        infoToggle.setAttribute('aria-expanded', 'false');
      });
    }
  }

  var isSending = false;
  var retryCount = 0;
  var isLocalHost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  var isFileProtocol = window.location.protocol === 'file:';
  var API_URL = window.MHM_CHATBOT_API_URL
    || (isLocalHost || isFileProtocol
      ? 'http://localhost:5001/api/chat'
      : 'https://api.milehighmovement.com:8443/api/chat');

  submitBtn.setAttribute('title', 'Send Message');
  submitBtn.setAttribute('data-tip', 'Send');

  var quickActionsWrap = document.getElementById('quickActionsWrap');
  if (quickActionsWrap && quickActionsWrap.parentNode) {
    quickActionsWrap.parentNode.removeChild(quickActionsWrap);
  }


  // Get timestamp in readable format
  function getTimestamp() {
    var now = new Date();
    var hours = String(now.getHours()).padStart(2, '0');
    var mins = String(now.getMinutes()).padStart(2, '0');
    return hours + ':' + mins;
  }

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function linkifyBotMessage(text) {
    var escaped = escapeHtml(text).replace(/\n/g, '<br>');

    escaped = escaped.replace(/\bhttps?:\/\/[^\s<]+/g, function(url) {
      var cleanUrl = url.replace(/&amp;/g, '&');
      return '<a href="' + cleanUrl + '" target="_blank" rel="noopener noreferrer">' + url + '</a>';
    });

    escaped = escaped.replace(/\b([A-Za-z0-9_-]+\.html)\b/g, function(path) {
      return '<a href="' + path + '" target="_blank" rel="noopener noreferrer">' + path + '</a>';
    });

    return escaped;
  }

  // Enhanced message addition with timestamps and status
  function addMessage(text, isUser, status) {
    var msg = document.createElement('div');
    msg.className = 'chat-message ' + (isUser ? 'user' : 'bot');
    if (status) msg.setAttribute('data-status', status);
    msg.setAttribute('role', 'article');

    var content = document.createElement('span');
    content.className = 'message-content';
    if (isUser) {
      content.textContent = text;
    } else {
      content.innerHTML = linkifyBotMessage(text);
    }

    var timestamp = document.createElement('span');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = getTimestamp();

    msg.appendChild(content);
    msg.appendChild(timestamp);

    messagesEl.appendChild(msg);
    messagesEl.scrollTop = messagesEl.scrollHeight;

    // Store in history
    messageHistory.push({
      text: text,
      isUser: isUser,
      timestamp: new Date().toISOString(),
      status: status
    });

    // Save history to localStorage
    try {
      localStorage.setItem(CHATBOT_CONFIG.HISTORY_KEY, JSON.stringify(messageHistory.slice(-50)));
    } catch (e) {
      console.warn('Could not save history to localStorage:', e);
    }

    return msg;
  }

  function addTyping() {
    var msg = document.createElement('div');
    msg.className = 'chat-message bot typing';
    msg.id = 'chat-typing';
    msg.setAttribute('role', 'status');
    msg.setAttribute('aria-live', 'polite');

    var dots = document.createElement('span');
    dots.className = 'typing-dots';
    dots.innerHTML = '<span>.</span><span>.</span><span>.</span>';

    msg.appendChild(dots);
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

  // Enhanced error messages based on error type
  function getErrorMessage(error, isRetry) {
    if (error && error.name === 'AbortError') {
      return isRetry 
        ? 'The request timed out again. Please check your connection and try again.'
        : 'The request timed out. Retrying...';
    }
    if (error && error.message === 'Network error') {
      return 'Network issue detected. Please check your internet connection.';
    }
    return 'I cannot connect to the server. Please make sure the backend is running.';
  }

  // Enhanced sendMessage with retry logic and better error handling
  function sendMessage() {
    var message = inputEl.value.trim();
    if (!message || isSending) return;

    setSending(true);
    addMessage(message, true, 'sent');
    inputEl.value = '';
    retryCount = 0;

    // Clear localStorage draft
    localStorage.removeItem(CHATBOT_CONFIG.STORAGE_KEY);

    // Track question for analytics
    var keywordMatch = message.match(/\b(calendar|event|activity|mission|origin|contact|phone|email|program|cost|kids|culinary|sports|outdoor|wellness|fitness|social|seasonal|community|chatbot)\b/gi);
    if (keywordMatch) {
      keywordMatch.forEach(function(keyword) {
        var key = keyword.toLowerCase();
        questionFrequency[key] = (questionFrequency[key] || 0) + 1;
      });
    }

    addTyping();
    attemptSendMessage(message);
  }

  function attemptSendMessage(message) {
    var controller = new AbortController();
    var timeoutId = setTimeout(function() { controller.abort(); }, CHATBOT_CONFIG.REQUEST_TIMEOUT_MS);

    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: message }),
      signal: controller.signal
    })
      .then(function(response) {
        clearTimeout(timeoutId);
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.json();
      })
      .then(function(data) {
        removeTyping();
        if (data && data.status === 'success' && data.response) {
          addMessage(String(data.response), false, 'received');
        } else {
          addMessage('I ran into an issue processing your request. Please try again.', false, 'error');
        }
      })
      .catch(function(error) {
        removeTyping();
        var errorMsg = getErrorMessage(error, retryCount > 0);
        
        if (error && error.name === 'AbortError' && retryCount < CHATBOT_CONFIG.MAX_RETRIES) {
          retryCount++;
          addMessage(errorMsg, false, 'retry');
          var backoffDelay = CHATBOT_CONFIG.RETRY_BACKOFF_MS * Math.pow(2, retryCount - 1);
          setTimeout(function() {
            addTyping();
            attemptSendMessage(message);
          }, backoffDelay);
        } else {
          addMessage(errorMsg, false, 'error');
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

  inputEl.addEventListener('input', function() {
    setSending(false);
    // Auto-save draft to localStorage
    var draft = inputEl.value.trim();
    if (draft) {
      try {
        localStorage.setItem(CHATBOT_CONFIG.STORAGE_KEY, draft);
      } catch (e) {
        console.warn('Could not save draft to localStorage:', e);
      }
    } else {
      localStorage.removeItem(CHATBOT_CONFIG.STORAGE_KEY);
    }
  });

  inputEl.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Enhanced accessibility: Allow Escape to close info widget
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && infoWidget && infoWidget.style.display !== 'none') {
      infoWidget.style.display = 'none';
      if (infoToggle) infoToggle.setAttribute('aria-expanded', 'false');
    }
  });

  setSending(false);

  // Log analytics on page unload
  window.addEventListener('beforeunload', function() {
    if (Object.keys(questionFrequency).length > 0) {
      try {
        var analytics = {
          timestamp: new Date().toISOString(),
          questions: questionFrequency,
          totalMessages: messageHistory.length
        };
        var existingAnalytics = JSON.parse(localStorage.getItem(CHATBOT_CONFIG.ANALYTICS_KEY) || '[]');
        existingAnalytics.push(analytics);
        localStorage.setItem(CHATBOT_CONFIG.ANALYTICS_KEY, JSON.stringify(existingAnalytics.slice(-100)));
      } catch (e) {
        console.warn('Could not save analytics:', e);
      }
    }
  });
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
