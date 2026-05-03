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
    var modeToggleButton = document.getElementById('modeToggleButton');
    var voiceMicButton = document.getElementById('voiceMicButton');

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
      infoToggle.type = 'button';
      infoToggle.setAttribute('aria-label', 'Show chatbot help');
      infoToggle.setAttribute('title', 'Help');
      infoToggle.innerHTML = '<span>?</span>';
      controls.appendChild(infoToggle);
    } else {
      infoToggle.setAttribute('aria-label', 'Show chatbot help');
      infoToggle.setAttribute('title', 'Help');
    }

    if (!modeToggleButton) {
      modeToggleButton = document.createElement('button');
      modeToggleButton.id = 'modeToggleButton';
      modeToggleButton.type = 'button';
      modeToggleButton.setAttribute('aria-label', 'Toggle hands-free voice mode');
      modeToggleButton.setAttribute('aria-pressed', 'false');
      modeToggleButton.setAttribute('title', 'Enable hands-free voice mode');
      modeToggleButton.innerHTML = '<span>Mode</span>';
      controls.appendChild(modeToggleButton);
    } else {
      modeToggleButton.setAttribute('aria-label', 'Toggle hands-free voice mode');
      if (!modeToggleButton.innerHTML || modeToggleButton.innerHTML.trim().length === 0) {
        modeToggleButton.innerHTML = '<span>Mode</span>';
      }
    }

    if (closeIcon && closeIcon.parentNode !== controls) {
      controls.appendChild(closeIcon);
    }
    if (closeIcon) {
      closeIcon.setAttribute('aria-label', 'Close chat');
      closeIcon.setAttribute('title', 'Close chat');
      closeIcon.setAttribute('tabindex', '0');
      closeIcon.setAttribute('role', 'button');
      closeIcon.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          closeChat();
        }
      });
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
        + '<li><b>Voice-only mode:</b> <br><span style="opacity:0.9;">Tap "Voice" in the top controls to start hands-free mode, then tap "Chat" to switch back.</span></li>'
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
        + '<li><b>Voice-only mode:</b> <br><span style="opacity:0.9;">Tap "Voice" in the top controls to start hands-free mode, then tap "Chat" to switch back.</span></li>'
        + '<li><b>General tips:</b> <br><span style="opacity:0.9;">Use keywords like "kids", "culinary", "sports", or "outdoor" for best results.</span></li>'
        + '</ul>';
    }

    var voiceModeStatus = document.getElementById('voiceModeStatus');
    if (!voiceModeStatus) {
      voiceModeStatus = document.createElement('div');
      voiceModeStatus.id = 'voiceModeStatus';
      voiceModeStatus.style.display = 'none';
      chatWindow.insertBefore(voiceModeStatus, messagesEl);
    }

    var voiceModeStatusText = document.getElementById('voiceModeStatusText');
    if (!voiceModeStatusText) {
      voiceModeStatusText = document.createElement('span');
      voiceModeStatusText.id = 'voiceModeStatusText';
      voiceModeStatusText.textContent = 'Voice-only mode active.';
      voiceModeStatus.appendChild(voiceModeStatusText);
    }

    var voicePicker = document.getElementById('voicePicker');
    if (!voicePicker) {
      voicePicker = document.createElement('select');
      voicePicker.id = 'voicePicker';
      voicePicker.setAttribute('aria-label', 'Choose voice');
      voicePicker.setAttribute('title', 'Choose voice');
      EDGE_TTS_VOICES.forEach(function(v) {
        var opt = document.createElement('option');
        opt.value = v.id;
        opt.textContent = v.label;
        if (v.id === selectedTTSVoice) opt.selected = true;
        voicePicker.appendChild(opt);
      });
      if (!selectedTTSVoice) voicePicker.selectedIndex = 0;
      voicePicker.addEventListener('change', function() {
        selectedTTSVoice = voicePicker.value;
        try { localStorage.setItem('chatbot_tts_voice', selectedTTSVoice); } catch (e) {}
      });
      voiceModeStatus.appendChild(voicePicker);
    }

    var infoClose = document.getElementById('infoClose');
    if (infoToggle && infoWidget) {
      infoToggle.addEventListener('click', function() {
        var widget = document.getElementById('infoWidget');
        if (widget) {
          widget.style.display = widget.style.display === 'none' ? 'block' : 'none';
        }
      });
    }
    if (infoClose && infoWidget) {
      infoClose.addEventListener('click', function() {
        var widget = document.getElementById('infoWidget');
        if (widget) {
          widget.style.display = 'none';
        }
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
  var READY_URL = API_URL.replace('/api/chat', '/api/ready');
  var TTS_URL = API_URL.replace('/api/chat', '/api/tts');
  var ttsAudio = null;
  var EDGE_TTS_VOICES = [
    { id: 'en-US-AriaNeural',  label: 'Aria (US Female)' },
    { id: 'en-US-JennyNeural', label: 'Jenny (US Female)' },
    { id: 'en-US-AnaNeural',   label: 'Ana (US Female)' },
    { id: 'en-US-GuyNeural',   label: 'Guy (US Male)' }
  ];
  var selectedTTSVoice = '';
  try {
    selectedTTSVoice = localStorage.getItem('chatbot_tts_voice') || '';
  } catch (e) { selectedTTSVoice = ''; }

  var SpeechRecognitionCtor = window.SpeechRecognition || window.webkitSpeechRecognition;
  var voiceRecognitionSupported = !!SpeechRecognitionCtor;
  var voiceSynthesisSupported = !!(window.speechSynthesis && window.SpeechSynthesisUtterance);
  var isListening = false;
  var recognition = null;
  var voiceOutputEnabled = false;
  var isVoiceOnlyMode = false;
  var voiceOnlyAutoListen = false;
  var isSpeaking = false;
  var voiceLoopTimer = null;
  var previousVoiceOutputEnabled = null;
  var speechVoices = [];
  var selectedVoiceURI = '';
  var speechRunToken = 0;
  var chatbotReady = false;
  var readyCheckInterval = null;

  // Voice output is only used in voice-only mode
  voiceOutputEnabled = false;

  try {
    selectedVoiceURI = localStorage.getItem('chatbot_selected_voice_uri') || '';
  } catch (e) {
    selectedVoiceURI = '';
  }

  // Create and show warmup banner
  var warmupBanner = document.createElement('div');
  warmupBanner.id = 'chatbot-warmup-banner';
  warmupBanner.style.cssText = 'background:#f0f0f0;border-bottom:1px solid #ccc;padding:10px;text-align:center;font-size:14px;color:#666;display:none;';
  warmupBanner.innerHTML = '⏳ Chatbot is starting up... Please wait.';
  if (messagesEl && messagesEl.parentNode) {
    messagesEl.parentNode.insertBefore(warmupBanner, messagesEl);
  }

  // Poll the /api/ready endpoint
  function pollReady() {
    fetch(READY_URL)
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (data && data.ready) {
          chatbotReady = true;
          warmupBanner.style.display = 'none';
          if (readyCheckInterval) {
            clearInterval(readyCheckInterval);
            readyCheckInterval = null;
          }
        } else {
          chatbotReady = false;
          warmupBanner.style.display = 'block';
        }
      })
      .catch(function() {
        chatbotReady = false;
        warmupBanner.style.display = 'block';
      });
  }

  // Start polling immediately
  pollReady();
  readyCheckInterval = setInterval(pollReady, 1000);

  function addMessage(text, isUser, method) {
    var msg = document.createElement('div');
    msg.className = 'chat-message ' + (isUser ? 'user' : 'bot');
    msg.textContent = text;
    
    // Add method label for bot responses if provided
    if (!isUser && method) {
      var methodLabel = document.createElement('div');
      methodLabel.className = 'message-method-label';
      methodLabel.textContent = method === 'llm' ? '(from LLM)' : '(from website)';
      msg.appendChild(methodLabel);
    }
    
    messagesEl.appendChild(msg);
    messagesEl.scrollTop = messagesEl.scrollHeight;

    if (!isUser) {
      speakBotReply(text);
    }
  }

  function isChatOpen() {
    return chatRoot && chatRoot.classList.contains('open');
  }

  function clearVoiceLoopTimer() {
    if (voiceLoopTimer) {
      clearTimeout(voiceLoopTimer);
      voiceLoopTimer = null;
    }
  }

  function setVoiceModeStatus(text, state) {
    var statusEl = document.getElementById('voiceModeStatus');
    var textEl = document.getElementById('voiceModeStatusText');
    if (!statusEl) return;
    if (!isVoiceOnlyMode || !text) {
      statusEl.style.display = 'none';
      statusEl.classList.remove('is-listening', 'is-speaking', 'is-paused');
      return;
    }
    if (textEl) {
      textEl.textContent = text;
    }
    statusEl.classList.remove('is-listening', 'is-speaking', 'is-paused');
    if (state === 'listening') {
      statusEl.classList.add('is-listening');
    } else if (state === 'speaking') {
      statusEl.classList.add('is-speaking');
    } else if (state === 'paused') {
      statusEl.classList.add('is-paused');
    }
    statusEl.style.display = 'block';
  }

  function getVoicePickerEl() {
    return document.getElementById('voicePicker');
  }

  function getPreferredVoiceScore(voice) {
    var score = 0;
    var name = (voice.name || '').toLowerCase();
    var lang = (voice.lang || '').toLowerCase();

    if (lang.indexOf('en') === 0) score += 30;
    if (lang.indexOf('en-us') === 0) score += 20;
    if (voice.localService) score += 6;

    var strongPreferred = ['aria', 'jenny', 'guy', 'davis', 'samantha', 'alex', 'ava', 'emma', 'alloy', 'nova', 'neural'];
    var weakPreferred = ['google', 'microsoft', 'enhanced', 'premium', 'natural'];
    var avoid = ['compact', 'espeak', 'festival', 'pipe', 'robot'];

    var i;
    for (i = 0; i < strongPreferred.length; i++) {
      if (name.indexOf(strongPreferred[i]) !== -1) score += 12;
    }
    for (i = 0; i < weakPreferred.length; i++) {
      if (name.indexOf(weakPreferred[i]) !== -1) score += 5;
    }
    for (i = 0; i < avoid.length; i++) {
      if (name.indexOf(avoid[i]) !== -1) score -= 12;
    }

    return score;
  }

  function getEnglishVoices() {
    var voices = speechVoices || [];
    return voices.filter(function(v) {
      var lang = (v.lang || '').toLowerCase();
      return lang.indexOf('en') === 0;
    });
  }

  function getBestVoice() {
    var englishVoices = getEnglishVoices();
    if (!englishVoices.length) return null;

    englishVoices.sort(function(a, b) {
      return getPreferredVoiceScore(b) - getPreferredVoiceScore(a);
    });
    return englishVoices[0] || null;
  }

  function resolveSelectedVoice() {
    var englishVoices = getEnglishVoices();
    if (!englishVoices.length) return null;

    if (selectedVoiceURI) {
      var exact = englishVoices.find(function(v) { return v.voiceURI === selectedVoiceURI; });
      if (exact) return exact;
    }
    return getBestVoice();
  }

  function updateVoicePickerOptions() {
    var picker = getVoicePickerEl();
    if (!picker) return;

    var englishVoices = getEnglishVoices();
    picker.innerHTML = '';

    if (!voiceSynthesisSupported || !englishVoices.length) {
      var unsupported = document.createElement('option');
      unsupported.value = '';
      unsupported.textContent = 'Default voice';
      picker.appendChild(unsupported);
      picker.disabled = true;
      return;
    }

    picker.disabled = false;

    englishVoices.sort(function(a, b) {
      return getPreferredVoiceScore(b) - getPreferredVoiceScore(a);
    });

    englishVoices.forEach(function(v) {
      var option = document.createElement('option');
      option.value = v.voiceURI;
      option.textContent = v.name + ' (' + v.lang + ')';
      picker.appendChild(option);
    });

    var selected = resolveSelectedVoice();
    if (selected) {
      selectedVoiceURI = selected.voiceURI;
      picker.value = selected.voiceURI;
      try {
        localStorage.setItem('chatbot_selected_voice_uri', selectedVoiceURI);
      } catch (e) {}
    }
  }

  function initVoicePicker() {
    var picker = getVoicePickerEl();
    if (!picker) return;

    picker.addEventListener('change', function() {
      selectedVoiceURI = picker.value || '';
      try {
        localStorage.setItem('chatbot_selected_voice_uri', selectedVoiceURI);
      } catch (e) {}
      if (isVoiceOnlyMode) {
        setVoiceModeStatus('Voice-only mode active. Voice updated.', 'paused');
        setTimeout(function() {
          if (isVoiceOnlyMode && !isSpeaking && !isListening) {
            setVoiceModeStatus('Voice-only mode active. Listening...', 'listening');
          }
        }, 800);
      }
    });

    if (!voiceSynthesisSupported || !window.speechSynthesis) {
      updateVoicePickerOptions();
      return;
    }

    speechVoices = window.speechSynthesis.getVoices() || [];
    updateVoicePickerOptions();

    window.speechSynthesis.onvoiceschanged = function() {
      speechVoices = window.speechSynthesis.getVoices() || [];
      updateVoicePickerOptions();
    };
  }

  function splitSpeechChunks(text) {
    var raw = String(text || '').replace(/\s+/g, ' ').trim();
    if (!raw) return [];

    var sentenceParts = raw.match(/[^.!?]+[.!?]*/g) || [raw];
    var chunks = [];
    var current = '';

    sentenceParts.forEach(function(part) {
      var next = part.trim();
      if (!next) return;

      if ((current + ' ' + next).trim().length > 170) {
        if (current) chunks.push(current.trim());
        current = next;
      } else {
        current = (current ? current + ' ' : '') + next;
      }
    });

    if (current) chunks.push(current.trim());
    return chunks;
  }

  function setModeToggleState() {
    var modeBtn = document.getElementById('modeToggleButton');
    if (!modeBtn) return;

    var actionLabel = isVoiceOnlyMode ? 'Chat' : 'Mode';
    modeBtn.innerHTML = '<span>' + actionLabel + '</span>';
    modeBtn.classList.toggle('is-voice-only', isVoiceOnlyMode);
    modeBtn.setAttribute('aria-pressed', isVoiceOnlyMode ? 'true' : 'false');
    modeBtn.setAttribute('aria-label', isVoiceOnlyMode ? 'Switch to chat mode' : 'Enable hands-free voice mode');
    modeBtn.setAttribute('title', isVoiceOnlyMode ? 'Return to chat mode' : 'Enable hands-free voice mode');
  }

  function stopListening() {
    clearVoiceLoopTimer();
    if (!recognition || !isListening) return;
    try {
      recognition.stop();
    } catch (e) {}
  }

  function startListening() {
    if (!voiceRecognitionSupported || !recognition || isListening || isSending || isSpeaking || !isChatOpen()) {
      return;
    }

    stopSpeechOutput();
    try {
      recognition.start();
    } catch (e) {}
  }

  function scheduleVoiceOnlyListen(delayMs) {
    clearVoiceLoopTimer();
    if (!isVoiceOnlyMode || !voiceOnlyAutoListen) return;
    voiceLoopTimer = setTimeout(function() {
      startListening();
    }, delayMs || 0);
  }

  function switchChatMode(nextMode, silent) {
    var mode = nextMode === 'voice-only' ? 'voice-only' : 'chat';
    if (mode === 'voice-only') {
      if (!voiceRecognitionSupported) {
        addMessage('Voice-only mode is not supported in this browser. Chat mode is still available.', false);
        return;
      }

      isVoiceOnlyMode = true;
      voiceOnlyAutoListen = true;
      previousVoiceOutputEnabled = voiceOutputEnabled;
      voiceOutputEnabled = true;

      chatRoot.classList.add('voice-only-mode');
      formEl.classList.add('voice-only-hidden');
      setVoiceModeStatus('Voice-only mode active. Listening...', 'listening');
      scheduleVoiceOnlyListen(150);

      if (!silent) {
        addMessage('Voice mode on. Speak naturally.', false);
      }
    } else {
      isVoiceOnlyMode = false;
      voiceOnlyAutoListen = false;
      stopListening();

      chatRoot.classList.remove('voice-only-mode');
      formEl.classList.remove('voice-only-hidden');
      setVoiceModeStatus('', 'paused');

      if (previousVoiceOutputEnabled !== null) {
        voiceOutputEnabled = previousVoiceOutputEnabled;
        previousVoiceOutputEnabled = null;
      }

      if (!silent) {
        addMessage('Back to chat mode.', false);
      }
    }

    setModeToggleState();
    try {
      localStorage.setItem('chatbot_mode', mode);
    } catch (e) {}
  }

  function getKnownActivityFallback(query, responseText) {
    var normalizedResponse = String(responseText || '').trim().toLowerCase();
    if (normalizedResponse !== 'i do not see that listed on the site.' && normalizedResponse !== 'i do not see that listed on the site') {
      return null;
    }

    var q = String(query || '').toLowerCase();

    if (q.indexOf('pickleball') !== -1) {
      return [
        'Here are the closest matches:',
        '- PICKLEBALL - Dedicated courts for friendly games and community matches. Equipment is provided and beginner instruction is available for newcomers. (Sports)',
        '- Take me there: sportsDirectory.html'
      ].join('\n');
    }

    if (q.indexOf('basketball') !== -1) {
      return [
        'Here are the closest matches:',
        '- BASKETBALL - Full-size indoor court available for open play, practice and scheduled pickup games. Features quality hoops and seating, ideal for players of all ages and skill levels. (Sports)',
        '- Take me there: sportsDirectory.html'
      ].join('\n');
    }

    return null;
  }

  function updateMicButtonState() {
    var micBtn = document.getElementById('voiceMicButton');
    if (!micBtn) return;

    if (!voiceRecognitionSupported) {
      micBtn.disabled = true;
      micBtn.classList.remove('is-listening');
      micBtn.setAttribute('aria-label', 'Voice input not supported');
      micBtn.setAttribute('title', 'Voice input not supported in this browser');
      micBtn.setAttribute('aria-pressed', 'false');
      return;
    }

    micBtn.disabled = false;
    micBtn.classList.toggle('is-listening', isListening);
    if (isVoiceOnlyMode) {
      micBtn.setAttribute('aria-label', isListening ? 'Pause voice-only listening' : 'Resume voice-only listening');
      micBtn.setAttribute('title', isListening ? 'Pause listening' : 'Resume listening');
      micBtn.innerHTML = '<span>' + (isListening ? 'Pause' : 'Talk') + '</span>';
    } else {
      micBtn.setAttribute('aria-label', isListening ? 'Stop one-time voice input' : 'Start one-time voice input');
      micBtn.setAttribute('title', isListening ? 'Stop listening' : 'Talk once (speech to text)');
      micBtn.innerHTML = '<span>' + (isListening ? 'Stop' : 'Talk') + '</span>';
    }
    micBtn.setAttribute('aria-pressed', isListening ? 'true' : 'false');
  }

  function stopSpeechOutput() {
    speechRunToken += 1;
    isSpeaking = false;
    if (ttsAudio) {
      ttsAudio.pause();
      ttsAudio.src = '';
      ttsAudio = null;
    }
    if (voiceSynthesisSupported) window.speechSynthesis.cancel();
  }

  function speakBotReply(text) {
    if (!voiceOutputEnabled && !isVoiceOnlyMode) return;
    if (!text) {
      if (isVoiceOnlyMode && voiceOnlyAutoListen) scheduleVoiceOnlyListen(350);
      return;
    }

    stopSpeechOutput();
    var activeToken = speechRunToken;
    isSpeaking = true;
    if (isVoiceOnlyMode) setVoiceModeStatus('Voice-only mode active. Speaking...', 'speaking');

    fetch(TTS_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text, voice: selectedTTSVoice || undefined })
    })
    .then(function(res) {
      if (!res.ok) throw new Error('tts ' + res.status);
      return res.blob();
    })
    .then(function(blob) {
      if (activeToken !== speechRunToken) return;
      var url = URL.createObjectURL(blob);
      var audio = new Audio(url);
      ttsAudio = audio;
      audio.onended = function() {
        URL.revokeObjectURL(url);
        ttsAudio = null;
        if (activeToken !== speechRunToken) return;
        isSpeaking = false;
        if (isVoiceOnlyMode && voiceOnlyAutoListen) {
          setVoiceModeStatus('Voice-only mode active. Listening...', 'listening');
          scheduleVoiceOnlyListen(300);
        }
      };
      audio.onerror = function() {
        URL.revokeObjectURL(url);
        ttsAudio = null;
        if (activeToken !== speechRunToken) return;
        fallbackSpeakBotReply(text, activeToken);
      };
      audio.play().catch(function() {
        if (activeToken !== speechRunToken) return;
        fallbackSpeakBotReply(text, activeToken);
      });
    })
    .catch(function() {
      if (activeToken !== speechRunToken) return;
      fallbackSpeakBotReply(text, activeToken);
    });
  }

  function fallbackSpeakBotReply(text, activeToken) {
    if (!voiceSynthesisSupported || !text) {
      isSpeaking = false;
      if (isVoiceOnlyMode && voiceOnlyAutoListen) {
        scheduleVoiceOnlyListen(350);
      }
      return;
    }

    var chunks = splitSpeechChunks(text);
    if (!chunks.length) {
      isSpeaking = false;
      if (isVoiceOnlyMode && voiceOnlyAutoListen) {
        scheduleVoiceOnlyListen(250);
      }
      return;
    }

    var token = activeToken !== undefined ? activeToken : speechRunToken;
    var chosenVoice = resolveSelectedVoice();

    function finishSpeechRun() {
      if (token !== speechRunToken) return;
      isSpeaking = false;
      if (isVoiceOnlyMode && voiceOnlyAutoListen) {
        setVoiceModeStatus('Voice-only mode active. Listening...', 'listening');
        scheduleVoiceOnlyListen(200);
      }
    }

    function speakChunk(index) {
      if (token !== speechRunToken) return;
      if (index >= chunks.length) {
        finishSpeechRun();
        return;
      }

      var utterance = new window.SpeechSynthesisUtterance(chunks[index]);
      utterance.rate = 0.94;
      utterance.pitch = 0.95;
      utterance.lang = chosenVoice && chosenVoice.lang ? chosenVoice.lang : 'en-US';
      if (chosenVoice) utterance.voice = chosenVoice;

      utterance.onstart = function() {
        if (token !== speechRunToken) return;
        isSpeaking = true;
        if (isVoiceOnlyMode) setVoiceModeStatus('Voice-only mode active. Speaking...', 'speaking');
      };
      utterance.onend = function() {
        if (token !== speechRunToken) return;
        setTimeout(function() { speakChunk(index + 1); }, 80);
      };
      utterance.onerror = function() {
        if (token !== speechRunToken) return;
        setTimeout(function() { speakChunk(index + 1); }, 50);
      };

      window.speechSynthesis.speak(utterance);
    }

    speakChunk(0);
  }

  function initVoiceRecognition() {
    if (!voiceRecognitionSupported) {
      updateMicButtonState();
      return;
    }

    recognition = new SpeechRecognitionCtor();
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = true;

    recognition.onstart = function() {
      isListening = true;
      if (isVoiceOnlyMode) {
        setVoiceModeStatus('Voice-only mode active. Listening...', 'listening');
      }
      updateMicButtonState();
    };

    recognition.onend = function() {
      isListening = false;
      updateMicButtonState();

      if (isVoiceOnlyMode && voiceOnlyAutoListen && !isSending && !isSpeaking && isChatOpen()) {
        scheduleVoiceOnlyListen(250);
      }
    };

    recognition.onresult = function(event) {
      var transcript = '';
      var hasFinal = false;
      var i;

      for (i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
        if (event.results[i].isFinal) hasFinal = true;
      }

      transcript = transcript.trim();
      if (!transcript) return;

      inputEl.value = transcript;
      setSending(false);

      if (hasFinal) {
        sendMessage();
      }
    };

    recognition.onerror = function(event) {
      isListening = false;
      updateMicButtonState();

      if (!event || !event.error) {
        addMessage('Voice input failed. Please try again.', false);
        return;
      }

      if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
        addMessage('Microphone access was denied. You can keep using text chat.', false);
        if (isVoiceOnlyMode) {
          switchChatMode('chat', true);
          addMessage('Switched back to chat mode because microphone access is required for voice-only mode.', false);
        }
      } else if (event.error === 'no-speech') {
        addMessage('No speech detected. Please try again.', false);
      } else {
        addMessage('Voice input error: ' + event.error + '. Please try again.', false);
      }
    };

    updateMicButtonState();
  }

  function toggleVoiceInput() {
    if (!voiceRecognitionSupported || !recognition) {
      addMessage('Voice input is not supported in this browser.', false);
      return;
    }

    if (isVoiceOnlyMode) {
      if (isListening) {
        voiceOnlyAutoListen = false;
        stopListening();
        setVoiceModeStatus('Voice mode paused. Tap Talk to resume.', 'paused');
      } else {
        voiceOnlyAutoListen = true;
        setVoiceModeStatus('Voice mode active. Listening...', 'listening');
        scheduleVoiceOnlyListen(0);
      }
      updateMicButtonState();
      return;
    }

    if (isListening) {
      recognition.stop();
      return;
    }

    stopSpeechOutput();
    try {
      recognition.start();
    } catch (e) {
      addMessage('Voice input could not start. Please try again.', false);
    }
  }

  function toggleVoiceOutput() {
    if (isVoiceOnlyMode) {
      addMessage('Voice-only mode keeps spoken replies on. Switch to chat mode to change this setting.', false);
      return;
    }

    voiceOutputEnabled = !voiceOutputEnabled;
    try {
      localStorage.setItem('chatbot_voice_output_enabled', voiceOutputEnabled ? '1' : '0');
    } catch (e) {}

    if (!voiceOutputEnabled) {
      stopSpeechOutput();
    }

    addMessage(voiceOutputEnabled ? 'Spoken replies enabled.' : 'Spoken replies disabled.', false);
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

    // Guard: don't send if chatbot is not ready
    if (!chatbotReady) {
      addMessage('The chatbot is still starting up. Please wait...', false);
      return;
    }

    stopSpeechOutput();

    setSending(true);
    addMessage(message, true);
    inputEl.value = '';
    setSending(true);
    addTyping();

    var MAX_RETRIES = 3;
    var BASE_BACKOFF = 1000; // ms

    function attemptSend(attempt) {
      var willRetry = false;
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
          // Backend not ready yet — ask to retry
          if (data && (data.status === 'initializing' || (data.response && String(data.response).toLowerCase().indexOf('starting up') !== -1))) {
            if (attempt < MAX_RETRIES) {
              var wait = BASE_BACKOFF * Math.pow(2, attempt - 1);
              addMessage('Chatbot is starting up — retrying in ' + (wait/1000) + 's...', false);
              willRetry = true;
              setTimeout(function() { attemptSend(attempt + 1); }, wait);
              return;
            } else {
              addMessage('The chatbot is still starting up. Please try again shortly.', false);
              return;
            }
          }

          if (data && data.status === 'success' && data.response) {
            var responseText = String(data.response);
            var method = data.method || 'tfidf';  // Default to tfidf if not specified
            var fallbackText = getKnownActivityFallback(message, responseText);
            addMessage(fallbackText || responseText, false, method);
          } else {
            addMessage('I ran into an issue. Please try again.', false);
          }
        })
        .catch(function(error) {
          removeTyping();
          // If connection or network error, attempt retry
          var isAbort = error && error.name === 'AbortError';
          if ((isAbort || !error || !error.message) && attempt < MAX_RETRIES) {
            var wait = BASE_BACKOFF * Math.pow(2, attempt - 1);
            addMessage('Network issue detected — retrying in ' + (wait/1000) + 's...', false);
            willRetry = true;
            setTimeout(function() { attemptSend(attempt + 1); }, wait);
            return;
          }

          if (isAbort) {
            addMessage('The request timed out. Please try again.', false);
          } else {
            addMessage('I cannot connect to the server. Please make sure the backend is running.', false);
          }
        })
        .finally(function() {
          if (willRetry) return;

          setSending(false);
          inputEl.focus();
          if (isVoiceOnlyMode && voiceOnlyAutoListen && !isSpeaking) {
            scheduleVoiceOnlyListen(300);
          }
        });
    }

    attemptSend(1);
  }

  formEl.addEventListener('submit', function(e) {
    e.preventDefault();
    sendMessage();
  });
  submitBtn.addEventListener('click', sendMessage);
  var modeBtn = document.getElementById('modeToggleButton');
  if (modeBtn) {
    modeBtn.addEventListener('click', function(e) {
      e.preventDefault();
      switchChatMode(isVoiceOnlyMode ? 'chat' : 'voice-only', false);
    });
  }

  inputEl.addEventListener('input', function() { setSending(false); });
  inputEl.addEventListener('keydown', function(e) {
    if (e.altKey && (e.key === 's' || e.key === 'S')) {
      e.preventDefault();
      toggleVoiceOutput();
      return;
    }

    if (e.key === 'Enter') {
      e.preventDefault();
      sendMessage();
    }
  });

  document.addEventListener('keydown', function(e) {
    if (e.altKey && (e.key === 's' || e.key === 'S')) {
      e.preventDefault();
      toggleVoiceOutput();
    }
  });

  initVoiceRecognition();
  initVoicePicker();
  switchChatMode('chat', true);
  setSending(false);

  window.__chatbotVoiceController = {
    onOpen: function() {
      if (isVoiceOnlyMode && voiceOnlyAutoListen) {
        scheduleVoiceOnlyListen(200);
      }
    },
    onClose: function() {
      clearVoiceLoopTimer();
      stopListening();
      stopSpeechOutput();
      if (isVoiceOnlyMode) {
        setVoiceModeStatus('Voice-only mode active. Paused while chat is closed.', 'paused');
      }
    }
  };
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initChatbotUI);
} else {
  initChatbotUI();
}

// Functions to open/close chatbot (for other UI triggers)
function openChat() {
  document.getElementById("chatbot").classList.add("open");
  if (window.__chatbotVoiceController && typeof window.__chatbotVoiceController.onOpen === 'function') {
    window.__chatbotVoiceController.onOpen();
  }
}

function closeChat() {
  if (window.__chatbotVoiceController && typeof window.__chatbotVoiceController.onClose === 'function') {
    window.__chatbotVoiceController.onClose();
  }
  document.getElementById("chatbot").classList.remove("open");
}
