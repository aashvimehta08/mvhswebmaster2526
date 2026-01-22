"""
Custom Chatbot for Mile High Movement Website
Main chatbot class that integrates all components
"""

import os
import re
import json
from datetime import datetime
from content_extractor import load_all_html_files, extract_structured_content
from custom_tfidf import CustomTFIDFVectorizer
from response_generator import ResponseGenerator


class CustomChatbot:
    """Custom chatbot that answers questions using website content"""
    
    def __init__(self, website_directory):
        self.website_directory = website_directory
        self.html_content = {}
        self.documents = []
        self.document_metadata = []
        self.vectorizer = CustomTFIDFVectorizer()
        self.response_generator = ResponseGenerator()
        self.contact_info = {
            'phone': '720-487-3920',
            'email': 'milehighmovement@gmail.com',
            'address': '3782 Movement Circle'
        }
        self.events = {}
        self.faqs = {}
        self.directories = {}
        self.activities = []
        self.mission_text = ""
        self.history = []  # Conversation history
        self._load_and_index_content()
    
    def _load_calendar_events(self):
        """Load events from calendar.js"""
        calendar_path = os.path.join(self.website_directory, '..', 'calendar.js')
        if os.path.exists(calendar_path):
            try:
                with open(calendar_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract events object
                events_match = re.search(r'const events = \{(.*?)\};', content, re.DOTALL)
                if events_match:
                    events_str = events_match.group(1)
                    # Parse date and events
                    date_pattern = r'"([\d-]+)":\s*\[(.*?)\]'
                    for match in re.finditer(date_pattern, events_str, re.DOTALL):
                        date = match.group(1)
                        events_list = re.findall(r'"([^"]+)"', match.group(2))
                        if events_list:
                            self.events[date] = events_list
                    print(f"Loaded {len(self.events)} event dates from calendar")
            except Exception as e:
                print(f"Error loading calendar events: {e}")
    
    def _load_faqs(self):
        """Load FAQs from aboutus.html"""
        aboutus_path = os.path.join(self.website_directory, 'aboutus.html')
        if os.path.exists(aboutus_path):
            try:
                with open(aboutus_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract FAQ items
                faq_pattern = r'<summary class="faqItemTitle">([^<]+)</summary>\s*<p[^>]*class="faqItemText">([^<]+)</p>'
                faq_matches = re.findall(faq_pattern, content, re.IGNORECASE)
                
                for i, (question, answer) in enumerate(faq_matches):
                    self.faqs[question.strip()] = answer.strip()
                    # Also add as searchable document
                    self.documents.append(f"FAQ: {question.strip()}. {answer.strip()}")
                    self.document_metadata.append({
                        'filename': 'aboutus.html',
                        'type': 'faq',
                        'question': question.strip(),
                        'answer': answer.strip()
                    })
                
                print(f"Loaded {len(self.faqs)} FAQs")
            except Exception as e:
                print(f"Error loading FAQs: {e}")

    def _load_mission(self):
        """Load mission statement from aboutus.html"""
        aboutus_path = os.path.join(self.website_directory, 'aboutus.html')
        if os.path.exists(aboutus_path):
            try:
                with open(aboutus_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                mission_pattern = r'<h1[^>]*>\s*MISSION STATEMENT\s*</h1>\s*<p[^>]*>(.*?)</p>'
                mission_match = re.search(mission_pattern, content, re.IGNORECASE | re.DOTALL)
                if mission_match:
                    mission_text = re.sub(r'<[^>]+>', '', mission_match.group(1)).strip()
                    if mission_text:
                        self.mission_text = mission_text
                        self.documents.append(f"Mission statement: {mission_text}")
                        self.document_metadata.append({
                            'filename': 'aboutus.html',
                            'type': 'mission',
                            'content': mission_text
                        })
            except Exception as e:
                print(f"Error loading mission statement: {e}")

    def _load_activities(self):
        """Load activities from directory pages"""
        self.activities = []
        for filename in os.listdir(self.website_directory):
            if not filename.endswith('Directory.html'):
                continue
            file_path = os.path.join(self.website_directory, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                titles = re.findall(r'class="[^"]*eventTitle[^"]*"[^>]*>(.*?)</h[12]>', content, re.IGNORECASE | re.DOTALL)
                texts = re.findall(r'class="[^"]*eventText[^"]*"[^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)

                titles = [re.sub(r'<[^>]+>', '', t).strip() for t in titles if t.strip()]
                texts = [re.sub(r'<[^>]+>', '', t).strip() for t in texts if t.strip()]

                category = filename.replace('Directory.html', '').lower()
                for i, title in enumerate(titles):
                    description = texts[i] if i < len(texts) else ''
                    if not title:
                        continue
                    activity = {
                        'title': title,
                        'description': description,
                        'category': category,
                        'source': filename
                    }
                    self.activities.append(activity)
                    doc = f"Activity: {title}. {description} Category: {category}."
                    self.documents.append(doc)
                    self.document_metadata.append({
                        'filename': filename,
                        'type': 'activity',
                        'title': title,
                        'content': description,
                        'category': category
                    })
            except Exception as e:
                print(f"Error loading activities from {filename}: {e}")
    
    def _load_and_index_content(self):
        """Load HTML files and create search index"""
        print("Loading website content...")
        self.html_content = load_all_html_files(self.website_directory)

        # Reset documents for indexing
        self.documents = []
        self.document_metadata = []

        # Extract documents for indexing
        for filename, data in self.html_content.items():
            text = data['text']
            
            # Skip very short content (likely navigation or empty pages)
            if len(text) < 50:
                continue
            
            # Add full document
            self.documents.append(text)
            self.document_metadata.append({
                'filename': filename,
                'type': 'full',
                'structured': data['structured']
            })
            
            # Also add individual sections for better retrieval
            structured = data['structured']
            
            # Add paragraphs as separate documents for better matching
            for para in structured.get('paragraphs', []):
                if len(para) > 20:
                    self.documents.append(para)
                    self.document_metadata.append({
                        'filename': filename,
                        'type': 'paragraph',
                        'content': para
                    })
            
            # Add headings + content pairs
            headings = structured.get('headings', [])
            paragraphs = structured.get('paragraphs', [])
            items = structured.get('items', [])
            
            for i, item in enumerate(items[:5]):  # Limit items
                if i < len(paragraphs):
                    combined = f"{item}. {paragraphs[i]}"
                    if len(combined) > 20:
                        self.documents.append(combined)
                        self.document_metadata.append({
                            'filename': filename,
                            'type': 'item',
                            'title': item,
                            'content': paragraphs[i]
                        })

        # Load events and FAQs after base content is indexed
        self._load_calendar_events()
        self._load_faqs()
        self._load_mission()
        self._load_activities()
        
        print(f"Indexed {len(self.documents)} content segments")
        
        # Train TF-IDF vectorizer
        print("Building search index...")
        self.vectorizer.fit(self.documents)
        print("Index built successfully!")
    
    def _extract_contact_info(self, query):
        """Extract and format contact information"""
        query_lower = query.lower()
        
        if 'phone' in query_lower or 'call' in query_lower or 'number' in query_lower:
            return f"Phone: {self.contact_info['phone']}"
        elif 'email' in query_lower or 'mail' in query_lower:
            return f"Email: {self.contact_info['email']}"
        elif 'address' in query_lower or 'location' in query_lower or 'where' in query_lower:
            return f"Address: {self.contact_info['address']}"
        else:
            return f"Phone: {self.contact_info['phone']}, Email: {self.contact_info['email']}, Address: {self.contact_info['address']}"
    
    def _get_upcoming_events(self, query):
        """Find events matching the query"""
        query_lower = query.lower()
        matching_events = []
        
        for date, events_list in sorted(self.events.items()):
            for event in events_list:
                event_lower = event.lower()
                # Check if query keywords match event
                keywords = query_lower.split()
                if any(keyword in event_lower for keyword in keywords if len(keyword) > 2):
                    matching_events.append(f"{date}: {event}")
        
        return matching_events[:5]  # Return top 5 matching events
    
    def _find_faq_match(self, query):
        """Find matching FAQ for query"""
        query_lower = query.lower()
        query_words = set(re.findall(r'\b[a-z]+\b', query_lower))
        stopwords = {'the', 'a', 'an', 'and', 'or', 'to', 'of', 'in', 'on', 'for', 'with', 'is', 'are', 'do', 'does', 'can', 'we', 'our', 'you', 'your'}
        query_words = {w for w in query_words if w not in stopwords}

        # Direct keyword routing for core FAQs
        if any(w in query_lower for w in ['types of programs', 'what programs', 'programs do you offer']):
            for faq_question, faq_answer in self.faqs.items():
                if 'types of programs' in faq_question.lower():
                    return faq_answer
        if any(w in query_lower for w in ['who can participate', 'who can attend', 'who is allowed']):
            for faq_question, faq_answer in self.faqs.items():
                if 'who can participate' in faq_question.lower():
                    return faq_answer
        if any(w in query_lower for w in ['cost', 'fee', 'price', 'pricing', 'membership cost']):
            for faq_question, faq_answer in self.faqs.items():
                if 'cost to participate' in faq_question.lower() or 'use the facilities' in faq_question.lower():
                    return faq_answer
        
        # Calculate similarity with FAQ questions
        for faq_question, faq_answer in self.faqs.items():
            question_lower = faq_question.lower()
            question_words = set(re.findall(r'\b[a-z]+\b', question_lower))
            question_words = {w for w in question_words if w not in stopwords}

            # If significant overlap, return the answer
            if len(query_words & question_words) >= 2:
                return faq_answer
            # Fuzzy fallback
            if len(query_words & question_words) == 1 and len(query_words) >= 3:
                return faq_answer
        
        return None
    
    def _suggest_directories(self, query):
        """Suggest relevant directory pages based on query"""
        query_lower = query.lower()
        
        directories = {
            'fitness': 'fitnessDirectory.html - Browse fitness classes and training programs',
            'sports': 'sportsDirectory.html - Explore sports activities and tournaments',
            'wellness': 'wellnessDirectory.html - Discover wellness and health programs',
            'kids': 'kidsDirectory.html - Activities and programs for children',
            'social': 'socialDirectory.html - Social events and community gatherings',
            'outdoor': 'outdoorDirectory.html - Outdoor activities and adventures',
            'culinary': 'culinaryDirectory.html - Cooking classes and food-related events',
            'seasonal': 'seasonalDirectory.html - Seasonal programs and special events'
        }
        
        suggestions = []
        for keyword, directory in directories.items():
            if keyword in query_lower:
                suggestions.append(directory)
        
        return suggestions

    def _search_activities(self, query):
        """Search activities by keyword and category"""
        query_lower = query.lower()
        tokens = re.findall(r'\b[a-z]+\b', query_lower)
        stopwords = {'the', 'a', 'an', 'and', 'or', 'to', 'of', 'in', 'on', 'for', 'with', 'is', 'are', 'do', 'does', 'can', 'we', 'our', 'you', 'your', 'about', 'any'}
        tokens = [t for t in tokens if t not in stopwords]

        if not tokens or (len(tokens) <= 2 and 'activity' in query_lower):
            return {'type': 'general', 'matches': []}

        matches = []
        for activity in self.activities:
            haystack = f"{activity['title']} {activity['description']} {activity['category']}".lower()
            score = sum(1 for t in tokens if t in haystack)
            if score > 0:
                matches.append((score, activity))

        matches.sort(key=lambda x: x[0], reverse=True)
        return {'type': 'matches', 'matches': [m[1] for m in matches[:6]]}
    
    def _retrieve_relevant_content(self, query, top_k=3):
        """Retrieve relevant content for a query"""
        # Check for contact information queries first
        query_lower = query.lower()
        if any(word in query_lower for word in ['contact', 'phone', 'email', 'address', 'location', 'locate', 'where', 'reach', 'call']):
            return [{'content': self._extract_contact_info(query), 'filename': 'contact', 'type': 'contact'}]

        # Direct mission lookup to avoid noisy retrieval
        if 'mission' in query_lower:
            if self.mission_text:
                return [{'content': self.mission_text, 'filename': 'aboutus.html', 'type': 'mission'}]

        # Activity queries
        if any(word in query_lower for word in ['activity', 'activities', 'things to do', 'classes', 'programs', 'what do you offer']):
            if self.activities:
                activity_search = self._search_activities(query)
                if activity_search['type'] == 'general':
                    categories = {}
                    for activity in self.activities:
                        categories.setdefault(activity['category'], []).append(activity['title'])
                    parts = []
                    for category, titles in categories.items():
                        sample = ', '.join(titles[:2])
                        parts.append(f"{category.capitalize()}: {sample}")
                    content = "ACTIVITY_CATEGORIES:" + "||".join(parts[:6])
                    return [{'content': content, 'filename': 'directories', 'type': 'activity_list'}]

                if activity_search['matches']:
                    parts = []
                    for activity in activity_search['matches']:
                        desc = activity['description']
                        if desc:
                            parts.append(f"{activity['title']} - {desc} ({activity['category'].capitalize()})")
                        else:
                            parts.append(f"{activity['title']} ({activity['category'].capitalize()})")
                    content = "ACTIVITY_MATCHES:" + "||".join(parts)
                    return [{'content': content, 'filename': 'directories', 'type': 'activity_list'}]
        
        # Check for FAQ matches
        faq_answer = self._find_faq_match(query)
        if faq_answer:
            return [{'content': faq_answer, 'filename': 'aboutus.html', 'type': 'faq'}]
        
        # Check for event queries
        if any(word in query_lower for word in ['event', 'schedule', 'when', 'time', 'class', 'activity']):
            upcoming_events = self._get_upcoming_events(query)
            if upcoming_events:
                event_content = "Here are some upcoming events: " + "; ".join(upcoming_events)
                return [{'content': event_content, 'filename': 'calendar.js', 'type': 'event'}]
        
        # Check for directory suggestions
        directory_suggestions = self._suggest_directories(query)
        if directory_suggestions:
            dir_content = "You might want to check out: " + ", ".join(directory_suggestions)
            return [{'content': dir_content, 'filename': 'directories', 'type': 'navigation'}]
        
        # Use TF-IDF to find similar documents
        try:
            similarities = self.vectorizer.find_most_similar(query, top_k=top_k)
            
            results = []
            for idx, similarity_score in similarities:
                if similarity_score > 0.01:  # Minimum similarity threshold
                    metadata = self.document_metadata[idx]
                    content = self.documents[idx]
                    
                    results.append({
                        'content': content,
                        'similarity': similarity_score,
                        'filename': metadata['filename'],
                        'type': metadata.get('type', 'full'),
                        'metadata': metadata
                    })
            
            # If no relevant results found, provide fallback
            if not results:
                return [{'content': "I'm not sure I understand that question. Could you rephrase it or ask about our programs, events, or contact information?", 'filename': 'low_confidence', 'type': 'fallback'}]
            
            return results
        except Exception as e:
            print(f"Error retrieving content: {e}")
            return [{'content': "I'm having trouble finding information right now. Please try again later.", 'filename': 'error', 'type': 'fallback'}]
    
    def ask(self, query):
        """Main method to ask the chatbot a question"""
        if not query or not query.strip():
            return "Please ask me a question about Mile High Movement community center!"
        
        query = query.strip()
        
        # Check for follow-up queries
        query_lower = query.lower()
        if query_lower in ['tell me more', 'more info', 'elaborate', 'expand', 'details'] and self.history:
            last = self.history[-1]
            return f"More about your previous question '{last['query']}': {last['response']}"
        
        # Retrieve relevant content
        retrieved_results = self._retrieve_relevant_content(query, top_k=3)
        
        # Combine retrieved content
        combined_content = self.response_generator.combine_multiple_results(retrieved_results)
        
        # Generate response
        response = self.response_generator.generate_response(query, combined_content)
        
        # Add to history
        self.history.append({'query': query, 'response': response})
        self.history = self.history[-5:]  # Keep last 5
        
        return response
    
    def get_events(self):
        """Get all events"""
        return dict(sorted(self.events.items()))  # Sort by date
