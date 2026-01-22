# Quick Start Guide - Custom Chatbot

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Backend Server
```bash
cd chatbot
python3 app.py
```

You should see:
```
Starting Custom Chatbot Server...
Chatbot is ready to answer questions!
 * Running on http://0.0.0.0:5000
```

### Step 3: Open the Chat Interface
Open `chatbot.html` in your web browser.

That's it! The chatbot is now ready to answer questions about your website.

## 📝 Test the Chatbot

Try asking:
- "What programs do you offer?"
- "What is your phone number?"
- "Tell me about fitness classes"
- "Where are you located?"

## 🔗 Adding to Your Website Navigation

To add a chatbot link to your navigation, you can add this to any HTML file:

```html
<div id="chatbot" class="icon">
  <a href="chatbot.html"><img id="chatbotIcon" class="iconImg" src="chatbot.png">
  <div class="line"></div>
  <p id="chatbotLabel" class="label">Chatbot</p></a>
</div>
```

Or simply add a link anywhere:
```html
<a href="chatbot.html">Chat with Us</a>
```

## 🛠 Troubleshooting

**Server won't start?**
- Make sure Flask is installed: `pip install flask flask-cors`
- Check that Python 3 is being used: `python3 --version`

**Chatbot shows error messages?**
- Make sure the backend server is running on port 5000
- Check browser console for errors (F12)
- Verify that `chatbot.html` and the `chatbot/` folder are in the same directory

**No responses from chatbot?**
- Make sure the server started successfully
- Check that HTML files are in the parent directory
- Look at the server console for error messages

## 📚 More Information

See `CHATBOT_README.md` for detailed documentation.


