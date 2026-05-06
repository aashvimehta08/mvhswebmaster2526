import re
import random
import difflib


class ResponseGenerator:
    
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
        for keyword in keywords:
            if difflib.SequenceMatcher(None, word.lower(), keyword.lower()).ratio() > threshold:
                return True
        return False
    
    def detect_intent(self, query):
        query_lower = query.lower()
        words = query_lower.split()
        
        for pattern in self.greeting_patterns:
            if re.search(pattern, query_lower):
                return 'greeting'

        for pattern in self.smalltalk_patterns:
            if re.search(pattern, query_lower):
                return 'smalltalk'
        
        contact_keywords = ['contact', 'phone', 'email', 'address', 'reach', 'call']
        if any(self.fuzzy_match_word(word, contact_keywords) for word in words):
            return 'contact'

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

        if any(phrase in query_lower for phrase in ['how did you begin', 'where did we begin', 'how did we begin', 'origin story', 'how it started']):
            return 'origin'

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
        query_lower = query.lower().strip()
        if len(query_lower) == 0:
            return True
        short_words = {'ok', 'okay', 'cool', 'nice', 'yeah', 'yep', 'no', 'sure', 'thanks', 'thank', 'lol', 'haha'}
        words = [w for w in re.findall(r'\b[a-z]+\b', query_lower)]
        if len(words) <= 2 and all(w in short_words for w in words):
            return True
        question_words = {'what', 'when', 'where', 'who', 'how', 'why', 'can', 'do', 'is', 'are', 'tell', 'show', 'about'}
        domain_prefixes = ('program', 'class', 'event', 'activit', 'fit', 'sport', 'wellness', 'kid', 'outdoor', 'culinary', 'season', 'contact', 'phone', 'email', 'address', 'hour', 'calendar', 'mission', 'origin')
        has_domain_word = any(any(w.startswith(prefix) for prefix in domain_prefixes) for w in words)
        if not any(w in question_words for w in words) and not has_domain_word:
            return True
        return False
    
    def extract_key_info(self, content, max_length=300):
        content = self.normalize_content(content)
        
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
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
                remaining = content[len(' '.join(result)):].strip()
                if remaining:
                    remaining = remaining[:max_length - current_length - 10]
                    if remaining:
                        text += '. ' + remaining
            return text + '.' if not text.endswith('.') else text
        
        return content[:max_length] + '...' if len(content) > max_length else content

    def is_reliable_content(self, content):
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
        content = self.normalize_content(content)
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
        content = self.normalize_content(content)
        address = re.search(r'\d{2,6}\s+[A-Za-z0-9\s.\-]+\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Circle|Cir|Lane|Ln|Drive|Dr|Way|Court|Ct)\b', content, re.IGNORECASE)
        if address:
            return f"\n- Address: {address.group(0)}"
        return ''
    
    def generate_response(self, query, retrieved_content):
        intent = self.detect_intent(query)

        if isinstance(retrieved_content, str) and retrieved_content.startswith("HAVE_QUERY_MATCHES:"):
            raw = retrieved_content.replace("HAVE_QUERY_MATCHES:", "", 1)
            parts = [p.strip() for p in raw.split("||") if p.strip()]
            if len(parts) >= 2:
                subject = parts[0]
                matches = parts[1:]
                bullets = '\n' + '\n'.join([f"- {m}" for m in matches[:6]])
                return f"Yes, we have options related to {subject}:{bullets}"

        if isinstance(retrieved_content, str) and retrieved_content.startswith("HAVE_QUERY_NONE:"):
            subject = retrieved_content.replace("HAVE_QUERY_NONE:", "", 1).strip()
            return (
                f"I could not find a clear match for '{subject}'."
                "\nTry asking with a specific keyword, like 'do you have pickleball' or 'events on January 24th'."
            )

        if isinstance(retrieved_content, str) and retrieved_content.strip() == "LOW_CONFIDENCE":
            return (
                "I couldn't find an exact match yet. Which one do you want?"
                "\n- Events by date (example: events on January 24th)"
                "\n- Program category (example: kids activities)"
                "\n- Contact info (phone, email, or address)"
            )

        if isinstance(retrieved_content, str) and retrieved_content.startswith("EVENTS_ON_DATE:"):
            event_response = self.format_event_date_response(retrieved_content)
            if event_response:
                return event_response

        if isinstance(retrieved_content, str) and retrieved_content.startswith("ACTIVITY_"):
            activity_response = self.format_activity_response(retrieved_content)
            if activity_response:
                return activity_response

        if intent == 'greeting':
            return random.choice(self.response_templates['greeting'])

        if intent == 'smalltalk':
            return random.choice(self.response_templates['smalltalk'])

        if self.is_low_info_query(query):
            return (
                "I can help with events, programs, or contact info. Try one of these:"
                "\n- Show events on January 24th"
                "\n- Show kids activities"
                "\n- What is your phone number?"
            )

        if intent == 'contact':
            if retrieved_content:
                # Avoid sentence splitting here so emails like name@example.com are not broken.
                content_text = self.normalize_content(retrieved_content)
                contact_block = self.format_contact_info(content_text)
                if contact_block:
                    return "Here's the best way to reach us:" + contact_block
                return "I do not see contact details listed on the site."
            return "I could not find contact info on the site. Please check the contact page."

        if intent == 'policy':
            return (
                "I do not see that policy listed on the site."
                "\nPlease contact us for details: milehighmovement@gmail.com or 720-487-3920."
            )

        if intent == 'clarify':
            return "Please tell me what topic you want details on. I can help with programs, events, services, and contact info."

        if intent == 'date_specific':
            return random.choice(self.response_templates['date_specific'])

        if intent in {'hours', 'pricing', 'location', 'volunteer', 'accessibility', 'calendar', 'kids', 'wellness', 'outdoor', 'culinary', 'sports', 'fitness_classes', 'events', 'mission', 'origin'}:
            if retrieved_content:
                if intent in {'mission', 'origin'}:
                    content_text = self.normalize_content(retrieved_content)
                else:
                    content_text = self.extract_key_info(retrieved_content, max_length=240)
                if not self.is_reliable_content(content_text):
                    return (
                        "I could not find an exact match on the site."
                        "\nTry: events by date, a program category, or contact info."
                    )
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
                return (
                    "I could not find exact details for that."
                    "\nWould you like events, programs, or contact info instead?"
                )
            return (
                "I could not find that on the website yet."
                "\nTell me if you want events, programs, or contact info and I can guide you."
            )
        
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

        if not retrieved_content or len(retrieved_content) == 0:
            return (
                "I could not find that yet."
                "\nTry one of these: events on a date, a program type, or contact details."
            )

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

        if not self.is_reliable_content(retrieved_content):
            return (
                "I could not find a reliable match for that request."
                "\nPlease try a specific date, program type, or contact question."
            )
        html = "Here's what I found:"
        if any(grouped[cat] for cat in grouped) or other:
            for cat in ['Events', 'Programs', 'Contact']:
                if grouped[cat]:
                    html += f"\n{cat}:{self.format_bullets(' '.join(grouped[cat][:3]), max_items=3)}"
            if other:
                html += f"\nOther:{self.format_bullets(' '.join(other[:3]), max_items=3)}"
        else:
            return (
                "I could not find that on the site."
                "\nTry asking about events, programs, or contact info."
            )

        if not any(word in query.lower() for word in ['contact', 'phone', 'email', 'address']):
            html += "\nIf you want details on a specific item, ask for it."

        if any(word in query.lower() for word in ['time', 'timing', 'schedule', 'hours', 'open', 'close']):
            html = "Our hours are not listed on the website.\nPlease contact us at 720-487-3920 or milehighmovement@gmail.com for the most up-to-date schedule."

        return html

        content_text = self.extract_key_info(retrieved_content)

        templates = self.response_templates.get(intent, self.response_templates['default'])
        template = random.choice(templates)

        response = template.format(content=content_text)

        if len(response) > 150 and intent != 'contact':
            follow_ups = [
                " Is there anything specific you'd like to know more about?",
                " Would you like more details?",
                " Feel free to ask if you need more information!"
            ]
            response += random.choice(follow_ups)

        return response
    
    def combine_multiple_results(self, results):
        if not results:
            return ""
        
        combined = []
        seen_content = set()
        
        for result in results[:3]:
            content = result.get('content', '').strip()
            content_hash = content.lower()[:100]
            if content_hash not in seen_content and content:
                combined.append(content)
                seen_content.add(content_hash)
        
        return ' '.join(combined)

    def normalize_content(self, content):
        content = ' '.join(content.split())
        content = re.sub(r'\b[\w\-]+\.(html|png|jpg|jpeg|gif)\b', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\bhtml\b', '', content, flags=re.IGNORECASE)
        content = re.sub(r'([a-z])([A-Z])', r'\1 \2', content)
        content = re.sub(r'\s+', ' ', content).strip()
        return content

    def format_activity_response(self, content):
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

    def format_event_date_response(self, content):
        if not content.startswith("EVENTS_ON_DATE:"):
            return None
        raw = content.replace("EVENTS_ON_DATE:", "").strip()
        parts = [p.strip() for p in raw.split("||") if p.strip()]
        if not parts:
            return "I do not see events listed for that date."
        date = parts[0]
        events = parts[1:]
        if not events or events == ["NONE"]:
            return (
                f"I do not see events listed for {date}."
                "\nYou can ask for a nearby date, or say 'show all events for that date'."
            )
        bullets = '\n' + '\n'.join([f'- {e}' for e in events])
        return f"Events on {date}:" + bullets
