# Custom Chatbot API Documentation

## Overview
The Mile High Movement Chatbot provides a REST API for answering questions about the community center using custom NLP and content indexing.

## Endpoints

### POST /api/chat
Send a chat message and receive a response.

**Request:**
```json
{
  "message": "What programs do you offer?"
}
```

**Response:**
```json
{
  "response": "Based on our website, we offer fitness classes...",
  "status": "success"
}
```

**Error Response:**
```json
{
  "response": "Error message",
  "status": "error",
  "error": "Details"
}
```

### GET /api/status
Get chatbot statistics.

**Response:**
```json
{
  "status": "success",
  "data": {
    "html_files_loaded": 16,
    "documents_indexed": 114,
    "vocabulary_size": 644,
    "status": "ready"
  }
}
```

### GET /api/health
Health check.

**Response:**
```json
{
  "status": "healthy"
}
```

### GET /api/events
Get calendar events.

**Response:**
```json
{
  "events": {"2025-01-01": ["New Year Event"]},
  "status": "success"
}
```

### POST /api/feedback
Submit user feedback.

**Request:**
```json
{
  "rating": 5,
  "comment": "Great chatbot!"
}
```

**Response:**
```json
{
  "status": "success"
}
```

## Features
- Intent detection with fuzzy matching
- Conversation memory
- Lemmatization for better search
- Confidence scoring
- Input sanitization and rate limiting

## Deployment
Run with `python app.py` in production with Gunicorn or similar.