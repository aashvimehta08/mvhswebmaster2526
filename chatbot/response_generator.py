"""
Custom Response Generator
Generates natural responses based on retrieved content using templates and context
"""

import re
import random
import difflib


class ResponseGenerator:
    """Custom response generator using templates and context matching"""
    
    def __init__(self):
        self.greeting_patterns = [
            r'\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b',
            r'\b(what\'?s up|howdy|yo)\b'
        ]

        self.smalltalk_patterns = [
            r'\bhow are you\b',
            r'\bhow\'?s it going\b',
            r'\bhow are things\b',
            r'\bwhat\'?s up\b',
            r'\bhow do you do\b',
            r'\bwho are you\b',
            r'\bwhat can you do\b',
            r'\bcan you help\b',
            r'\bhelp me\b',
            r'\bthanks\b',
            r'\bthank you\b'
        ]
        
        self.question_patterns = {
            'what': r'\bwhat\b',
            'when': r'\bwhen\b',
            'where': r'\bwhere\b',
            'who': r'\bwho\b',
            'how': r'\bhow\b',
            'why': r'\bwhy\b',
            'can': r'\bcan\b',
            'do': r'\bdo\b',
            'is': r'\bis\b',
            'are': r'\bare\b',
            'tell': r'\btell\b',
            'show': r'\bshow\b',
            'about': r'\babout\b'
        }
        
        self.response_templates = {
            'greeting': [
                "Hello. What can I help you with today?",
                "Hi. What would you like to know about the community center?",
                "Welcome. What can I help you find?"
            ],
            'smalltalk': [
                "I'm doing well. What can I help you with?",
                "I'm here to help. What would you like to know?",
                "Thanks for asking. What can I help you find?"
            ],
            'about_center': [
                "Here's what I found: {content}",
                "This is what we have listed: {content}",
                "Here is the summary: {content}"
            ],
            'programs': [
                "We offer {content}. Would you like to know more about any specific program?",
                "Here are the programs we have: {content}",
                "Our programs include {content}"
            ],
            'contact': [
                "You can reach us at: {content}",
                "Contact information: {content}",
                "How to contact us: {content}"
            ],
            'hours': [
                "Hours: {content}",
                "Listed hours: {content}",
                "Hours information: {content}"
            ],
            'pricing': [
                "Pricing or membership: {content}",
                "Pricing details: {content}",
                "Membership information: {content}"
            ],
            'location': [
                "Location: {content}",
                "Location details: {content}",
                "How to find us: {content}"
            ],
            'volunteer': [
                "Volunteer or donation info: {content}",
                "Volunteer details: {content}",
                "Donation information: {content}"
            ],
            'accessibility': [
                "Accessibility information: {content}",
                "Accessibility details: {content}",
                "Accessibility notes: {content}"
            ],
            'calendar': [
                "Calendar: {content}",
                "Calendar information: {content}",
                "Events calendar: {content}"
            ],
            'kids': [
                "Kids programs: {content}",
                "Kids and family activities: {content}",
                "Youth programs: {content}"
            ],
            'wellness': [
                "Wellness programs: {content}",
                "Health and wellness: {content}",
                "Wellness offerings: {content}"
            ],
            'outdoor': [
                "Outdoor activities: {content}",
                "Outdoor programs: {content}",
                "Outdoor offerings: {content}"
            ],
            'culinary': [
                "Cooking and culinary: {content}",
                "Culinary programs: {content}",
                "Food-related classes: {content}"
            ],
            'sports': [
                "Sports programs: {content}",
                "Sports offerings: {content}",
                "Athletics and sports: {content}"
            ],
            'fitness_classes': [
                "Fitness classes: {content}",
                "Training programs: {content}",
                "Fitness offerings: {content}"
            ],
            'events': [
                "Events: {content}",
                "Events and activities: {content}",
                "Upcoming events: {content}"
            ],
            'mission': [
                "Mission statement: {content}",
                "Our mission: {content}",
                "Mission information: {content}"
            ],
            'date_specific': [
                "I do not see specific dates listed here. Please check the calendar or ask about a specific program.",
                "I do not see date-specific details on the site. Please check the calendar or name a program.",
                "I do not have a date-specific schedule. Please check the calendar or ask about a program."
            ],
            'default': [
                "I found this information: {content}",
                "Here's what I know: {content}",
                "According to our website: {content}"
            ]
        }
    
    def fuzzy_match_word(self, word, keywords, threshold=0.7):
        """Check if word is similar to any keyword using fuzzy matching"""
        for keyword in keywords:
            if difflib.SequenceMatcher(None, word.lower(), keyword.lower()).ratio() > threshold:
                return True
        return False
    
    def detect_intent(self, query):
        """Detect the intent of the user's query with fuzzy matching"""
        query_lower = query.lower()
        words = query_lower.split()
        
        # Check for greetings
        for pattern in self.greeting_patterns:
            if re.search(pattern, query_lower):
                return 'greeting'

        # Check for small talk
        for pattern in self.smalltalk_patterns:
            if re.search(pattern, query_lower):
                return 'smalltalk'
        
        # Check for contact queries first with fuzzy matching
        contact_keywords = ['contact', 'phone', 'email', 'address', 'reach', 'call']
        if any(self.fuzzy_match_word(word, contact_keywords) for word in words):
            return 'contact'

        # Common FAQ intents
        if any(word in query_lower for word in ['hours', 'open', 'close', 'opening', 'closing', 'schedule', 'time']):
            return 'hours'

        if any(word in query_lower for word in ['price', 'pricing', 'cost', 'fee', 'membership', 'rates', 'tuition', 'pay']):
            return 'pricing'

        if any(word in query_lower for word in ['location', 'address', 'where', 'directions', 'parking', 'map']):
            return 'location'

        if any(word in query_lower for word in ['volunteer', 'donate', 'donation', 'sponsor', 'support']):
            return 'volunteer'

        if any(word in query_lower for word in ['accessibility', 'accessible', 'wheelchair', 'ada', 'accommodations']):
            return 'accessibility'

        if any(word in query_lower for word in ['pet', 'pets', 'animal', 'dog', 'cat', 'service animal', 'service dog']):
            return 'policy'

        if any(word in query_lower for word in ['calendar', 'events calendar']):
            return 'calendar'

        if any(word in query_lower for word in ['kids', 'youth', 'family', 'children', 'teen']):
            return 'kids'

        if any(word in query_lower for word in ['wellness', 'health', 'meditation', 'mental']):
            return 'wellness'

        if any(word in query_lower for word in ['outdoor', 'trail', 'hiking', 'adventure', 'kayak', 'bike']):
            return 'outdoor'

        if any(word in query_lower for word in ['cooking', 'culinary', 'kitchen', 'food', 'baking']):
            return 'culinary'

        if any(word in query_lower for word in ['sports', 'tournament', 'league', 'tennis', 'pickleball', 'basketball', 'soccer']):
            return 'sports'

        if any(word in query_lower for word in ['fitness class', 'fitness classes', 'training', 'workout', 'gym', 'cardio', 'strength']):
            return 'fitness_classes'

        if any(word in query_lower for word in ['event', 'events', 'activities', 'activity']) and 'today' in query_lower:
            return 'date_specific'

        if any(word in query_lower for word in ['event', 'events', 'activities', 'activity']):
            return 'events'

        if any(word in query_lower for word in ['mission']):
            return 'mission'

        if any(word in query_lower for word in ['today', 'tomorrow', 'next', 'this week', 'this weekend', 'next week']):
            return 'date_specific'

        if any(word in query_lower for word in ['drop-in', 'drop in', 'dropins', 'drop ins', 'guests', 'guest']):
            return 'policy'

        if any(word in query_lower for word in ['refund', 'refunds', 'cancellation', 'cancel']):
            return 'policy'

        if any(word in query_lower for word in ['pool', 'swim', 'swimming']):
            return 'policy'

        if any(word in query_lower for word in ['repeat', 'tell me more', 'more details', 'what do you mean']):
            return 'clarify'
        
        # Check for question types
        if re.search(self.question_patterns['what'], query_lower):
            if 'program' in query_lower or 'offer' in query_lower or 'service' in query_lower:
                return 'programs'
            return 'about_center'
        
        if 'program' in query_lower or 'class' in query_lower or 'event' in query_lower or 'activity' in query_lower or 'fitness' in query_lower or 'sports' in query_lower or 'wellness' in query_lower or 'kids' in query_lower or 'outdoor' in query_lower or 'culinary' in query_lower or 'seasonal' in query_lower:
            return 'programs'
        
        if 'about' in query_lower or 'mission' in query_lower or 'who' in query_lower:
            return 'about_center'
        
        return 'default'

    def is_low_info_query(self, query):
        """Check if a query is too vague or short to retrieve useful content."""
        query_lower = query.lower().strip()
        if len(query_lower) == 0:
            return True
        # Very short inputs like "ok", "cool", "yeah", "nice"
        short_words = {'ok', 'okay', 'cool', 'nice', 'yeah', 'yep', 'no', 'sure', 'thanks', 'thank', 'lol', 'haha'}
        words = [w for w in re.findall(r'\b[a-z]+\b', query_lower)]
        if len(words) <= 2 and all(w in short_words for w in words):
            return True
        # No question words or domain keywords
        question_words = {'what', 'when', 'where', 'who', 'how', 'why', 'can', 'do', 'is', 'are', 'tell', 'show', 'about'}
        domain_keywords = {'program', 'class', 'event', 'activity', 'fitness', 'sports', 'wellness', 'kids', 'outdoor', 'culinary', 'seasonal', 'contact', 'phone', 'email', 'address', 'hours'}
        if not any(w in question_words for w in words) and not any(w in domain_keywords for w in words):
            return True
        return False
    
    def extract_key_info(self, content, max_length=300):
        """Extract key information from content, limiting length"""
        # Remove extra whitespace
        content = self.normalize_content(content)
        
        # Try to find sentences
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Take first few sentences that fit in max_length
        result = []
        current_length = 0
        
        for sentence in sentences:
            if current_length + len(sentence) + 1 <= max_length:
                result.append(sentence)
                current_length += len(sentence) + 1
            else:
                break
        
        if result:
            text = '. '.join(result)
            if current_length < max_length and len(content) > current_length:
                # Add a bit more if there's space
                remaining = content[len(' '.join(result)):].strip()
                if remaining:
                    remaining = remaining[:max_length - current_length - 10]
                    if remaining:
                        text += '. ' + remaining
            return text + '.' if not text.endswith('.') else text
        
        # Fallback: just truncate
        return content[:max_length] + '...' if len(content) > max_length else content

    def is_reliable_content(self, content):
        """Return True if content looks meaningful and not navigation noise."""
        if not content:
            return False
        content = ' '.join(content.split())
        if len(content) < 40:
            return False
        junk_markers = [
            'home directory about us feedback calendar', 'reference page',
            'your browser does not support the video tag', 'mile high movement',
            'where luxury begins', 'about us', 'ask here', 'send', 'chatbot'
        ]
        lower = content.lower()
        if any(marker in lower for marker in junk_markers):
            return False
        return True

    def format_bullets(self, content, max_items=4):
        """Format content into a short bullet list for readability (plain text)."""
        content = self.normalize_content(content)
        # Protect email addresses from being split on dots.
        email_placeholders = {}
        for idx, email in enumerate(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', content)):
            placeholder = f'__EMAIL_{idx}__'
            email_placeholders[placeholder] = email
            content = content.replace(email, placeholder)

        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        bullets = []
        junk_markers = [
            'home directory about us feedback calendar', 'reference page',
            'your browser does not support the video tag', 'mile high movement',
            'where luxury begins', 'about us'
        ]
        for sentence in sentences:
            if len(bullets) >= max_items:
                break
            lower_sentence = sentence.lower()
            if len(lower_sentence) < 10:
                continue
            if any(marker in lower_sentence for marker in junk_markers):
                continue
            if sentence not in bullets:
                bullets.append(sentence)
        if not bullets and content:
            bullets = [content[:160] + '...' if len(content) > 160 else content]
        # Restore emails in bullets.
        restored = []
        for bullet in bullets:
            for placeholder, email in email_placeholders.items():
                bullet = bullet.replace(placeholder, email)
            restored.append(bullet)
        bullets = restored
        if not bullets:
            return ''
        return '\n' + '\n'.join([f'- {b}' for b in bullets])

    def format_contact_info(self, content):
        """Extract and format contact details into clean bullets."""
        content = self.normalize_content(content)
        phone = re.search(r'(\+?1[\s\-\.]?)?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}', content)
        email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', content)
        address = re.search(r'\d{2,6}\s+[A-Za-z0-9\s.\-]+\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Circle|Cir|Lane|Ln|Drive|Dr|Way|Court|Ct)\b', content, re.IGNORECASE)

        bullets = []
        if phone:
            bullets.append(f"Phone: {phone.group(0)}")
        if email:
            bullets.append(f"Email: {email.group(0)}")
        if address:
            bullets.append(f"Address: {address.group(0)}")

        if bullets:
            return '\n' + '\n'.join([f'- {b}' for b in bullets])
        return ''

    def extract_address_only(self, content):
        """Return a formatted address bullet if one is found."""
        content = self.normalize_content(content)
        address = re.search(r'\d{2,6}\s+[A-Za-z0-9\s.\-]+\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Circle|Cir|Lane|Ln|Drive|Dr|Way|Court|Ct)\b', content, re.IGNORECASE)
        if address:
            return f"\n- Address: {address.group(0)}"
        return ''
    
    def generate_response(self, query, retrieved_content):
        """Generate a response based on query and retrieved content"""
        intent = self.detect_intent(query)

        if isinstance(retrieved_content, str) and retrieved_content.startswith("ACTIVITY_"):
            activity_response = self.format_activity_response(retrieved_content)
            if activity_response:
                return activity_response

        # Handle greetings
        if intent == 'greeting':
            return random.choice(self.response_templates['greeting'])

        # Handle small talk
        if intent == 'smalltalk':
            return random.choice(self.response_templates['smalltalk'])

        # Handle vague or low-information queries
        if self.is_low_info_query(query):
            return "I can help with programs, events, services, or contact info. What would you like to know?"

        # Handle contact queries directly
        if intent == 'contact':
            if retrieved_content:
                content_text = self.extract_key_info(retrieved_content, max_length=220)
                contact_block = self.format_contact_info(content_text)
                if contact_block:
                    return "Here's the best way to reach us:" + contact_block
                return "I do not see contact details listed on the site."
            return "I could not find contact info on the site. Please check the contact page."

        if intent == 'policy':
            return "I do not see that policy listed on the site. Please contact us for details."

        if intent == 'clarify':
            return "Please tell me what topic you want details on. I can help with programs, events, services, and contact info."

        if intent == 'date_specific':
            return random.choice(self.response_templates['date_specific'])

        # FAQ-style intents with scannable responses
        if intent in {'hours', 'pricing', 'location', 'volunteer', 'accessibility', 'calendar', 'kids', 'wellness', 'outdoor', 'culinary', 'sports', 'fitness_classes', 'events', 'mission'}:
            if retrieved_content:
                if intent == 'mission':
                    content_text = self.normalize_content(retrieved_content)
                else:
                    content_text = self.extract_key_info(retrieved_content, max_length=240)
                if not self.is_reliable_content(content_text):
                    return "I do not see that listed on the site."
                if intent == 'location':
                    address_block = self.extract_address_only(content_text)
                    if address_block:
                        return "Location:" + address_block
                    return "I do not see parking or location details listed on the site."
                templates = self.response_templates.get(intent, self.response_templates['default'])
                header = random.choice(templates).format(content='')
                header = header.replace(': ', ':').strip()
                bullets = self.format_bullets(content_text, max_items=6 if intent == 'mission' else 4)
                if bullets:
                    return f"{header}{bullets}"
                return "I do not see that listed on the site."
            return (
                "I do not see that listed on the website. Please share what you are looking for."
            )
        
        # Handle programs queries with a concise, scannable summary
        if intent == 'programs':
            if retrieved_content:
                summary = self.extract_key_info(retrieved_content, max_length=220)
                buckets = [
                    ("Fitness & Training", ['fitness', 'training', 'workout', 'gym', 'cardio', 'strength']),
                    ("Sports & Tournaments", ['sports', 'tournament', 'league', 'basketball', 'soccer', 'tennis', 'pickleball']),
                    ("Wellness & Health", ['wellness', 'health', 'meditation', 'mental', 'nutrition', 'massage']),
                    ("Kids & Families", ['kids', 'youth', 'teen', 'family', 'playroom']),
                    ("Social & Events", ['social', 'event', 'gathering', 'club', 'mixer', 'movie']),
                    ("Outdoor & Adventure", ['outdoor', 'trail', 'hiking', 'kayak', 'bike']),
                    ("Culinary & Food", ['cooking', 'culinary', 'kitchen', 'food', 'baking']),
                    ("Seasonal", ['seasonal', 'spring', 'summer', 'fall', 'winter', 'holiday'])
                ]

                found = []
                lower_summary = summary.lower()
                for label, keywords in buckets:
                    if any(keyword in lower_summary for keyword in keywords):
                        found.append(label)

                if found:
                    items = found[:6]
                    bullets = '\n' + '\n'.join([f'- {item}' for item in items])
                    return (
                        "Here are a few program areas you can explore:"
                        f"{bullets}"
                    )

                return (
                    "Here are a few program areas you can explore:"
                    "\n- Fitness & Training"
                    "\n- Sports & Tournaments"
                    "\n- Wellness & Health"
                    "\n- Kids & Families"
                    "\n- Outdoor & Adventure"
                    "\n- Culinary & Food"
                )

            return (
                "Here are a few program areas you can explore:"
                "\n- Fitness & Training"
                "\n- Sports & Tournaments"
                "\n- Wellness & Health"
                "\n- Kids & Families"
                "\n- Outdoor & Adventure"
                "\n- Culinary & Food"
            )

        # If no content retrieved, provide a helpful response
        if not retrieved_content or len(retrieved_content) == 0:
            return "I could not find that on the site. Please rephrase your question."

        # Remove navigation, branding, and repeated symbols
        nav_keywords = [
            'Home', 'Directory', 'About Us', 'Feedback', 'Calendar', 'Reference Page',
            'WELCOME', 'Your browser does not support the video tag.', 'MILE HIGH MOVEMENT',
            'WHERE LUXURY BEGINS', 'ABOUT US', '❀', 'logo.png', 'spacer.png',
            'Ask Here', 'Send', 'Chatbot', 'Ask me anything', 'Navigation', 'Submit'
        ]
        for nav in nav_keywords:
            retrieved_content = retrieved_content.replace(nav, '')
        retrieved_content = re.sub(r'\.{2,}', '.', retrieved_content)
        retrieved_content = re.sub(r'\s+', ' ', retrieved_content).strip()

        # Group by category if possible (simple keyword grouping)
        categories = {
            'Events': ['event', 'gathering', 'calendar', 'session', 'class', 'workshop', 'meeting'],
            'Programs': ['program', 'service', 'activity', 'arts', 'fitness', 'wellness', 'enrichment', 'playroom', 'tutoring', 'club'],
            'Contact': ['phone', 'email', 'address', 'contact'],
        }
        grouped = {cat: [] for cat in categories}
        other = []
        items = re.split(r'\n|;|\.|,|\u2022|- ', retrieved_content)
        seen = set()
        for i in items:
            clean = i.strip(' .:-')
            if clean and len(clean) > 6 and clean.lower() not in seen:
                found = False
                for cat, keywords in categories.items():
                    if any(kw in clean.lower() for kw in keywords):
                        grouped[cat].append(clean)
                        found = True
                        break
                if not found:
                    other.append(clean)
                seen.add(clean.lower())

        # Build response (scannable, plain text)
        if not self.is_reliable_content(retrieved_content):
            return "I do not see that listed on the site. Please rephrase your question."
        html = "Here's what I found:"
        if any(grouped[cat] for cat in grouped) or other:
            for cat in ['Events', 'Programs', 'Contact']:
                if grouped[cat]:
                    html += f"\n{cat}:{self.format_bullets(' '.join(grouped[cat][:3]), max_items=3)}"
            if other:
                html += f"\nOther:{self.format_bullets(' '.join(other[:3]), max_items=3)}"
        else:
            # If nothing useful was extracted, return a clean fallback instead of empty categories.
            return "I do not see that listed on the site. Please rephrase your question."

        # Add call-to-action or clarifying question
        if not any(word in query.lower() for word in ['contact', 'phone', 'email', 'address']):
            html += "\nIf you want details on a specific item, ask for it."

        # Fallback for timing queries
        if any(word in query.lower() for word in ['time', 'timing', 'schedule', 'hours', 'open', 'close']):
            html = "Our hours are not listed on the website.\nPlease contact us at 720-487-3920 or milehighmovement@gmail.com for the most up-to-date schedule."

        return html

        # Extract key information from retrieved content
        content_text = self.extract_key_info(retrieved_content)

        # Select appropriate template
        templates = self.response_templates.get(intent, self.response_templates['default'])
        template = random.choice(templates)

        # Format response
        response = template.format(content=content_text)

        # Add follow-up for longer responses
        if len(response) > 150 and intent != 'contact':
            follow_ups = [
                " Is there anything specific you'd like to know more about?",
                " Would you like more details?",
                " Feel free to ask if you need more information!"
            ]
            response += random.choice(follow_ups)

        return response
    
    def combine_multiple_results(self, results):
        """Combine multiple retrieved results into coherent content"""
        if not results:
            return ""
        
        combined = []
        seen_content = set()
        
        for result in results[:3]:  # Limit to top 3 results
            content = result.get('content', '').strip()
            # Simple deduplication
            content_hash = content.lower()[:100]
            if content_hash not in seen_content and content:
                combined.append(content)
                seen_content.add(content_hash)
        
        return ' '.join(combined)

    def normalize_content(self, content):
        """Normalize content to remove file names and layout artifacts."""
        content = ' '.join(content.split())
        # Remove file names like outdoorDirectory.html
        content = re.sub(r'\b[\w\-]+\.(html|png|jpg|jpeg|gif)\b', '', content, flags=re.IGNORECASE)
        # Remove stray "html" tokens left after splitting
        content = re.sub(r'\bhtml\b', '', content, flags=re.IGNORECASE)
        # Add spaces in camelCase identifiers (e.g., outdoorDirectory -> outdoor Directory)
        content = re.sub(r'([a-z])([A-Z])', r'\1 \2', content)
        # Clean up extra spaces
        content = re.sub(r'\s+', ' ', content).strip()
        return content

    def format_activity_response(self, content):
        """Format activity list content into bullets."""
        if content.startswith("ACTIVITY_CATEGORIES:"):
            raw = content.replace("ACTIVITY_CATEGORIES:", "").strip()
            parts = [p.strip() for p in raw.split("||") if p.strip()]
            if not parts:
                return "I do not see activities listed on the site."
            bullets = '\n' + '\n'.join([f'- {p}' for p in parts])
            return "Here are some activity areas:" + bullets

        if content.startswith("ACTIVITY_MATCHES:"):
            raw = content.replace("ACTIVITY_MATCHES:", "").strip()
            parts = [p.strip() for p in raw.split("||") if p.strip()]
            if not parts:
                return "I do not see that activity listed on the site."
            bullets = '\n' + '\n'.join([f'- {p}' for p in parts])
            return "Here are the closest matches:" + bullets

        return None
