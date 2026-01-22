"""
Unit tests for the Custom Chatbot
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot import CustomChatbot
from response_generator import ResponseGenerator


class TestCustomChatbot(unittest.TestCase):
    def setUp(self):
        # Use a test directory or mock
        self.chatbot = CustomChatbot(os.path.dirname(os.path.abspath(__file__)))

    def test_ask_contact(self):
        response = self.chatbot.ask("What is your phone number?")
        self.assertIn("Phone:", response)

    def test_ask_programs(self):
        response = self.chatbot.ask("What programs do you offer?")
        self.assertIn("fitness", response.lower())

    def test_ask_unknown(self):
        response = self.chatbot.ask("What is the meaning of life?")
        self.assertIn("not sure", response.lower())

    def test_history(self):
        self.chatbot.ask("Hello")
        response = self.chatbot.ask("tell me more")
        self.assertIn("previous question", response.lower())


class TestResponseGenerator(unittest.TestCase):
    def setUp(self):
        self.rg = ResponseGenerator()

    def test_detect_intent_contact(self):
        intent = self.rg.detect_intent("What is your phone?")
        self.assertEqual(intent, 'contact')

    def test_detect_intent_programs(self):
        intent = self.rg.detect_intent("What programs?")
        self.assertEqual(intent, 'programs')


if __name__ == '__main__':
    unittest.main()