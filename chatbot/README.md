# Custom Chatbot for Mile High Movement

This is a fully custom chatbot implementation that answers questions using content from the website. It uses:

- **Custom HTML Parser**: Extracts text content from HTML files
- **Custom TF-IDF Vectorizer**: Pure Python implementation for semantic search
- **Custom Response Generator**: Template-based response generation
- **Flask Backend**: REST API for chat interface
- **Modern Frontend**: Beautiful chat UI

## Installation

1. Install Python dependencies:
```bash
pip install -r ../requirements.txt
```

## Running the Chatbot

1. Start the backend server:
```bash
python app.py
```

The server will start on http://localhost:5000

2. Open `chatbot.html` in your browser or serve it through a web server.

## Architecture

- `content_extractor.py`: Extracts and parses HTML content
- `custom_tfidf.py`: Custom TF-IDF implementation for document similarity
- `response_generator.py`: Generates natural language responses
- `chatbot.py`: Main chatbot class that integrates all components
- `app.py`: Flask server that provides API endpoints

## Features

- No external AI APIs required
- Fully custom implementation
- Semantic search using TF-IDF
- Natural language responses
- Beautiful web interface


