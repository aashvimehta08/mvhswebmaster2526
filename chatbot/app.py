from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from chatbot import CustomChatbot

app = Flask(__name__)
CORS(app)

chatbot_dir = os.path.dirname(os.path.abspath(__file__))
website_directory = os.path.dirname(chatbot_dir)
chatbot = CustomChatbot(website_directory)


@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        query = data.get('message', '').strip()
        
        query = re.sub(r'\s+', ' ', query).strip()
        if len(query) > 500:
            logger.warning("Query too long")
            return jsonify({
                'response': 'Your question is too long. Please keep it under 500 characters.',
                'status': 'error'
            }), 400
        
        logger.info(f"Received chat query: {query}")
        
        if not query:
            logger.warning("Empty query received")
            return jsonify({
                'response': 'Please ask me a question about Mile High Movement community center!',
                'status': 'success'
            })
        
        response = chatbot.ask(query)
        logger.info(f"Generated response: {response[:100]}...")
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        return jsonify({
            'response': 'I apologize, but I encountered an error processing your request.',
            'status': 'error',
            'error': str(e)
        }), 500


@app.route('/api/status', methods=['GET'])
def status():
    try:
        status_info = chatbot.get_status()
        return jsonify({
            'status': 'success',
            'data': status_info
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})


@app.route('/api/version', methods=['GET'])
def version():
    return jsonify({'version': '1.0.0', 'name': 'Mile High Movement Chatbot'})


@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        events = chatbot.get_events()
        return jsonify({
            'events': events,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Error getting events: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@app.route('/api/feedback', methods=['POST'])
def feedback():
    try:
        data = request.get_json()
        rating = data.get('rating')
        comment = data.get('comment', '')
        logger.info(f"Feedback: rating={rating}, comment={comment}")
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Error processing feedback: {str(e)}")
        return jsonify({'status': 'error'}), 500


if __name__ == '__main__':
    print("Starting Custom Chatbot Server...")
    print("Chatbot is ready to answer questions!")
    app.run(debug=True, port=5001, host='0.0.0.0')

