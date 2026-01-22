# 🚀 Starting Your Chatbot

## Quick Start (3 Steps)

### Step 1: Install Flask (if not already installed)
Open Terminal and run:
```bash
pip3 install flask flask-cors
```

Or if you get permission errors, try:
```bash
pip3 install --user flask flask-cors
```

### Step 2: Start the Backend Server
Navigate to your project folder and run:
```bash
cd /Users/aarav.dwivedi2k9hotmail.com/Desktop/mvhswebmaster2526/chatbot
python3 app.py
```

You should see:
```
Starting Custom Chatbot Server...
Chatbot is ready to answer questions!
 * Running on http://0.0.0.0:5000
```

**Keep this terminal window open!** The server needs to keep running.

### Step 3: Open the Chat Interface
1. Open your web browser
2. Go to the file location: `/Users/aarav.dwivedi2k9hotmail.com/Desktop/mvhswebmaster2526/chatbot.html`
   - Or simply double-click `chatbot.html` in Finder
   - Or open it from your code editor

3. Start chatting! Try asking:
   - "What programs do you offer?"
   - "What is your phone number?"
   - "Tell me about fitness classes"

## ✅ That's It!

The chatbot is now running and ready to answer questions about your website!

## 🔧 Troubleshooting

**If you get "ModuleNotFoundError: No module named 'flask'":**
- Make sure you installed Flask: `pip3 install flask flask-cors`

**If the chatbot shows connection errors:**
- Make sure the backend server is running (Step 2)
- Check that it says "Running on http://0.0.0.0:5000"
- Make sure you haven't closed the terminal window

**If you want to stop the server:**
- Go to the terminal where it's running
- Press `Ctrl+C` to stop it

