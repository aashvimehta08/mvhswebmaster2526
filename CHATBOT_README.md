# Custom AI Chatbot for Mile High Movement Website

This is a **fully custom chatbot** built specifically for your website. It uses no external AI APIs - everything is implemented from scratch using pure Python.

## 🎯 Features

- **100% Custom Implementation**: No external AI services or APIs
- **Semantic Search**: Custom TF-IDF vectorizer for finding relevant content
- **Natural Responses**: Template-based response generation system
- **Beautiful UI**: Modern, responsive chat interface
- **Real-time**: Fast responses using indexed content

## 📁 Project Structure

```
chatbot/
├── content_extractor.py    # Extracts text from HTML files
├── custom_tfidf.py         # Custom TF-IDF implementation
├── response_generator.py   # Generates natural language responses
├── chatbot.py              # Main chatbot class
├── app.py                  # Flask backend server
└── test_chatbot.py         # Test script

chatbot.html                # Frontend chat interface
requirements.txt            # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
cd chatbot
python3 app.py
```

Or use the convenience script:
```bash
./run_chatbot.sh
```

The server will start on `http://localhost:5000`

### 3. Open the Chat Interface

Open `chatbot.html` in your web browser, or serve it through a web server.

You can also test the chatbot from command line:
```bash
cd chatbot
python3 test_chatbot.py
```

## 🔧 How It Works

### 1. Content Extraction
- Parses all HTML files in the website directory
- Extracts meaningful text content (headings, paragraphs, descriptions)
- Removes navigation, scripts, and other non-content elements

### 2. Indexing (TF-IDF)
- Builds a searchable index using Term Frequency-Inverse Document Frequency
- Creates vectors for all content segments
- Enables semantic similarity matching

### 3. Query Processing
- Tokenizes and processes user queries
- Finds most relevant content using cosine similarity
- Ranks results by relevance

### 4. Response Generation
- Uses template-based generation with context matching
- Formats responses naturally
- Handles different question types (greetings, information, contact, etc.)

## 💡 Example Questions

- "What programs do you offer?"
- "Tell me about fitness classes"
- "What is your phone number?"
- "Where are you located?"
- "What sports activities are available?"
- "Tell me about the community center"

## 🔌 API Endpoints

### POST `/api/chat`
Send a chat message and get a response.

**Request:**
```json
{
  "message": "What programs do you offer?"
}
```

**Response:**
```json
{
  "response": "We offer a wide mix of activities...",
  "status": "success"
}
```

### GET `/api/status`
Get chatbot status and statistics.

### GET `/api/health`
Health check endpoint.

## 🎨 Customization

The chatbot is fully customizable:

- **Response Templates**: Edit `response_generator.py` to change response styles
- **Search Algorithm**: Modify `custom_tfidf.py` to adjust search behavior
- **Content Extraction**: Update `content_extractor.py` to change what content is indexed
- **UI**: Customize `chatbot.html` to match your website design

## 📝 Technical Details

### No External AI APIs
This chatbot uses:
- Pure Python implementations
- Standard library HTML parsing
- Custom TF-IDF algorithm
- Template-based response generation
- No machine learning models or external APIs

### Dependencies
- Flask: Web server framework
- flask-cors: CORS support for frontend
- Python standard library: Everything else

## 🔍 How Search Works

1. User asks a question
2. Question is tokenized and converted to TF-IDF vector
3. Cosine similarity compares query vector with all document vectors
4. Top 3 most similar documents are retrieved
5. Relevant content is extracted and formatted into a response

## 🎯 Future Enhancements (Optional)

If you want to improve the chatbot later, you could add:
- Conversation history/memory
- Multi-turn conversations
- Better entity recognition
- Synonyms and related terms expansion
- Confidence scoring

## 📞 Support

The chatbot is ready to use! Just start the server and open the chat interface.

For questions or issues, check the code comments in each file for detailed explanations.


