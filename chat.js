// Simple Chatbot Popup Loader
(function() {
  if (window.__chatbotLoaded) return;
  window.__chatbotLoaded = true;

  // Create the chat icon button
  var chatBtn = document.createElement('div');
  chatBtn.id = 'chatbot-popup-btn';
  chatBtn.style.position = 'fixed';
  chatBtn.style.bottom = '32px';
  chatBtn.style.right = '32px';
  chatBtn.style.width = '60px';
  chatBtn.style.height = '60px';
  chatBtn.style.background = '#764ba2';
  chatBtn.style.borderRadius = '50%';
  chatBtn.style.boxShadow = '0 4px 16px rgba(0,0,0,0.2)';
  chatBtn.style.display = 'flex';
  chatBtn.style.justifyContent = 'center';
  chatBtn.style.alignItems = 'center';
  chatBtn.style.cursor = 'pointer';
  chatBtn.style.zIndex = '9999';
  chatBtn.innerHTML = '<span style="font-size: 2em; color: white;">💬</span>';

  // Create the iframe for the chatbot
  var chatIframe = document.createElement('iframe');
  chatIframe.id = 'chatbot-iframe';
  chatIframe.src = 'chatbot.html';
  chatIframe.style.position = 'fixed';
  chatIframe.style.bottom = '100px';
  chatIframe.style.right = '32px';
  chatIframe.style.width = '400px';
  chatIframe.style.height = '600px';
  chatIframe.style.border = 'none';
  chatIframe.style.borderRadius = '16px';
  chatIframe.style.boxShadow = '0 8px 32px rgba(0,0,0,0.25)';
  chatIframe.style.display = 'none';
  chatIframe.style.zIndex = '10000';

  // Toggle chatbot popup
  chatBtn.onclick = function() {
    chatIframe.style.display = (chatIframe.style.display === 'none') ? 'block' : 'none';
  };

  // Add to document
  document.body.appendChild(chatBtn);
  document.body.appendChild(chatIframe);
})();
