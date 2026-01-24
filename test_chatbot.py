"""
Simple test script for the custom chatbot
"""

import os
import sys

# Add chatbot directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot import CustomChatbot

def test_chatbot():
    """Test the chatbot with sample questions"""
    # Get the parent directory (website root)
    chatbot_dir = os.path.dirname(os.path.abspath(__file__))
    website_directory = os.path.dirname(chatbot_dir)
    
    print("Initializing chatbot...")
    chatbot = CustomChatbot(website_directory)
    
    print("\nChatbot initialized successfully!")
    print(f"Status: {chatbot.get_status()}\n")
    
    # Test questions
    test_questions = [
        "What programs do you offer?",
        "What is your phone number?",
        "Tell me about fitness classes",
        "What sports activities are available?",
        "Where are you located?",
        "Tell me about the community center"
    ]
    
    print("Testing chatbot with sample questions:\n")
    print("=" * 60)
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        print("-" * 60)
        response = chatbot.ask(question)
        print(f"Response: {response}\n")
        print("=" * 60)

if __name__ == '__main__':
    test_chatbot()


