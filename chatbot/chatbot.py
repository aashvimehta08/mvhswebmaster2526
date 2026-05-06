import os
import re
import json
from datetime import datetime, timedelta
from content_extractor import load_all_html_files, extract_structured_content
from custom_tfidf import CustomTFIDFVectorizer
from response_generator import ResponseGenerator

class CustomChatbot:
    
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
        self.origin_text = ""
        self.history = []
        self.last_event_date = None
        self._load_and_index_content()

    def _days_in_month(self, year, month):
        if month == 2:
            leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
            return 29 if leap else 28
        if month in {4, 6, 9, 11}:
            return 30
        return 31

    def _extract_event_topic_from_query(self, query_lower):
        topic_map = {
            'kids': ['kids', 'kid', 'children', 'child', 'youth', 'teen', 'family'],
            'sports': ['sports', 'basketball', 'soccer', 'tennis', 'pickleball', 'tournament'],
            'wellness': ['wellness', 'meditation', 'yoga', 'health'],
            'culinary': ['culinary', 'cooking', 'kitchen', 'baking', 'food'],
            'outdoor': ['outdoor', 'hiking', 'trail', 'kayak', 'bike', 'garden'],
            'social': ['social', 'mixer', 'movie', 'meetup', 'club']
        }
        for label, terms in topic_map.items():
            if any(term in query_lower for term in terms):
                return label
        return None

    def _filter_events_for_topic(self, events_list, topic_label):
        if not topic_label:
            return events_list

        topic_terms = {
            'kids': ['kids', 'kid', 'youth', 'teen', 'family', 'playroom', 'homework'],
            'sports': ['basketball', 'soccer', 'tennis', 'pickleball', 'tournament', 'gym', 'swim'],
            'wellness': ['meditation', 'yoga', 'wellness', 'health', 'recovery'],
            'culinary': ['cooking', 'kitchen', 'baking', 'culinary', 'food'],
            'outdoor': ['hiking', 'trail', 'kayak', 'bike', 'garden', 'outdoor', 'clean-up'],
            'social': ['social', 'mixer', 'movie', 'meetup', 'club', 'game night', 'wine tasting']
        }

        terms = topic_terms.get(topic_label, [])
        if not terms:
            return events_list

        filtered = [
            event for event in events_list
            if any(term in event.lower() for term in terms)
        ]
        return filtered

    def _rewrite_event_followup_query(self, query):
        query_lower = query.lower().strip()

        if self._parse_date_from_query(query):
            return query

        if not self.last_event_date:
            return query

        has_followup_time_ref = any(
            phrase in query_lower
            for phrase in [
                'tomorrow', 'next day', 'day after', 'yesterday', 'previous day',
                'next week', 'same day next month', 'that date'
            ]
        )

        if not has_followup_time_ref:
            return query

        has_event_context = any(
            phrase in query_lower
            for phrase in ['event', 'events', 'schedule', 'happening', 'what about', 'and on', 'that day']
        )

        if not has_event_context and self.history:
            has_event_context = self.history[-1].get('topic') == 'event'

        if not has_event_context:
            return query

        try:
            base_date = datetime.strptime(self.last_event_date, '%Y-%m-%d')
        except ValueError:
            return query

        day_offset = 0
        if 'day after' in query_lower:
            day_offset = 2
        elif 'next week' in query_lower:
            day_offset = 7
        elif 'tomorrow' in query_lower or 'next day' in query_lower:
            day_offset = 1
        elif 'yesterday' in query_lower or 'previous day' in query_lower:
            day_offset = -1

        if 'same day next month' in query_lower:
            year = base_date.year
            month = base_date.month + 1
            if month > 12:
                month = 1
                year += 1
            day = min(base_date.day, self._days_in_month(year, month))
            target_date = f"{year:04d}-{month:02d}-{day:02d}"
        else:
            target_date = (base_date + timedelta(days=day_offset)).strftime('%Y-%m-%d')

        topic_label = self._extract_event_topic_from_query(query_lower)
        if topic_label:
            return f"events on {target_date} for {topic_label}"
        return f"events on {target_date}"
    
    def _load_calendar_events(self):
        calendar_path = os.path.join(self.website_directory, 'calendar.js')
        if os.path.exists(calendar_path):
            try:
                with open(calendar_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                events_match = re.search(r'const events = \{(.*?)\};', content, re.DOTALL)
                if events_match:
                    events_str = events_match.group(1)
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
        aboutus_path = os.path.join(self.website_directory, 'aboutus.html')
        if os.path.exists(aboutus_path):
            try:
                with open(aboutus_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                faq_pattern = r'<summary class="faqItemTitle">([^<]+)</summary>\s*<p[^>]*class="faqItemText">([^<]+)</p>'
                faq_matches = re.findall(faq_pattern, content, re.IGNORECASE)
                
                for i, (question, answer) in enumerate(faq_matches):
                    self.faqs[question.strip()] = answer.strip()
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

    def _load_origin(self):
        aboutus_path = os.path.join(self.website_directory, 'aboutus.html')
        if os.path.exists(aboutus_path):
            try:
                with open(aboutus_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                origin_text = ""
                id_match = re.search(r'<p[^>]*id="whereFromText"[^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
                if id_match:
                    origin_text = re.sub(r'<[^>]+>', '', id_match.group(1)).strip()
                else:
                    origin_pattern = r'<h1[^>]*>\s*WHERE DID WE BEGIN\\?\\s*</h1>\\s*<p[^>]*>(.*?)</p>'
                    origin_match = re.search(origin_pattern, content, re.IGNORECASE | re.DOTALL)
                    if origin_match:
                        origin_text = re.sub(r'<[^>]+>', '', origin_match.group(1)).strip()

                if origin_text:
                    self.origin_text = origin_text
                    self.documents.append(f"Origin: {origin_text}")
                    self.document_metadata.append({
                        'filename': 'aboutus.html',
                        'type': 'origin',
                        'content': origin_text
                    })
            except Exception as e:
                print(f"Error loading origin story: {e}")

    def _load_activities(self):
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
        print("Loading website content...")
        self.html_content = load_all_html_files(self.website_directory)

        self.documents = []
        self.document_metadata = []

        for filename, data in self.html_content.items():
            text = data['text']
            
            if len(text) < 50:
                continue
            
            self.documents.append(text)
            self.document_metadata.append({
                'filename': filename,
                'type': 'full',
                'structured': data['structured']
            })
            
            structured = data['structured']
            
            for para in structured.get('paragraphs', []):
                if len(para) > 20:
                    self.documents.append(para)
                    self.document_metadata.append({
                        'filename': filename,
                        'type': 'paragraph',
                        'content': para
                    })
            
            headings = structured.get('headings', [])
            paragraphs = structured.get('paragraphs', [])
            items = structured.get('items', [])
            
            for i, item in enumerate(items[:5]):
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

        self._load_calendar_events()
        self._load_faqs()
        self._load_mission()
        self._load_origin()
        self._load_activities()
        
        print(f"Indexed {len(self.documents)} content segments")
        
        print("Building search index...")
        self.vectorizer.fit(self.documents)
        print("Index built successfully!")
    
    def _extract_contact_info(self, query):
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
        query_lower = query.lower()
        matching_events = []
        
        for date, events_list in sorted(self.events.items()):
            for event in events_list:
                event_lower = event.lower()
                keywords = query_lower.split()
                if any(keyword in event_lower for keyword in keywords if len(keyword) > 2):
                    matching_events.append(f"{date}: {event}")
        
        return matching_events[:5]

    def _parse_date_from_query(self, query):
        query_lower = query.lower()
        month_map = {
            'january': 1, 'jan': 1,
            'february': 2, 'feb': 2,
            'march': 3, 'mar': 3,
            'april': 4, 'apr': 4,
            'may': 5,
            'june': 6, 'jun': 6,
            'july': 7, 'jul': 7,
            'august': 8, 'aug': 8,
            'september': 9, 'sep': 9, 'sept': 9,
            'october': 10, 'oct': 10,
            'november': 11, 'nov': 11,
            'december': 12, 'dec': 12,
        }

        iso_match = re.search(r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b', query_lower)
        if iso_match:
            year, month, day = iso_match.groups()
            try:
                return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
            except ValueError:
                return None

        numeric_match = re.search(r'\b(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})\b', query_lower)
        if numeric_match:
            month, day, year = numeric_match.groups()
            year = int(year)
            if year < 100:
                year += 2000
            try:
                return f"{year:04d}-{int(month):02d}-{int(day):02d}"
            except ValueError:
                return None

        # MM/DD without year defaults to current year.
        numeric_no_year_match = re.search(r'\b(\d{1,2})[\/\-](\d{1,2})\b', query_lower)
        if numeric_no_year_match:
            month, day = numeric_no_year_match.groups()
            year = datetime.now().year
            try:
                return f"{year:04d}-{int(month):02d}-{int(day):02d}"
            except ValueError:
                return None

        word_match = re.search(r'\b([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?(?:,)?\s+(\d{4})\b', query_lower)
        if word_match:
            month_word, day, year = word_match.groups()
            month = month_map.get(month_word)
            if month:
                try:
                    return f"{int(year):04d}-{month:02d}-{int(day):02d}"
                except ValueError:
                    return None

        day_month_year_match = re.search(r'\b(\d{1,2})(?:st|nd|rd|th)?\s+([a-z]+)(?:,)?\s+(\d{4})\b', query_lower)
        if day_month_year_match:
            day, month_word, year = day_month_year_match.groups()
            month = month_map.get(month_word)
            if month:
                try:
                    return f"{int(year):04d}-{month:02d}-{int(day):02d}"
                except ValueError:
                    return None

        word_match_no_year = re.search(r'\b([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?\b', query_lower)
        if word_match_no_year:
            month_word, day = word_match_no_year.groups()
            month = month_map.get(month_word)
            if month:
                year = datetime.now().year
                try:
                    return f"{year:04d}-{month:02d}-{int(day):02d}"
                except ValueError:
                    return None

        day_month_no_year_match = re.search(r'\b(\d{1,2})(?:st|nd|rd|th)?\s+([a-z]+)\b', query_lower)
        if day_month_no_year_match:
            day, month_word = day_month_no_year_match.groups()
            month = month_map.get(month_word)
            if month:
                year = datetime.now().year
                try:
                    return f"{year:04d}-{month:02d}-{int(day):02d}"
                except ValueError:
                    return None

        return None
    
    def _find_faq_match(self, query):
        query_lower = query.lower()
        query_words = set(re.findall(r'\b[a-z]+\b', query_lower))
        stopwords = {'the', 'a', 'an', 'and', 'or', 'to', 'of', 'in', 'on', 'for', 'with', 'is', 'are', 'do', 'does', 'can', 'we', 'our', 'you', 'your'}
        query_words = {w for w in query_words if w not in stopwords}

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
        
        for faq_question, faq_answer in self.faqs.items():
            question_lower = faq_question.lower()
            question_words = set(re.findall(r'\b[a-z]+\b', question_lower))
            question_words = {w for w in question_words if w not in stopwords}

            if len(query_words & question_words) >= 2:
                return faq_answer
            if len(query_words & question_words) == 1 and len(query_words) >= 3:
                return faq_answer
        
        return None
    
    def _suggest_directories(self, query):
        query_lower = query.lower()
        
        directories = {
            'fitness': 'Fitness directory: Browse fitness classes and training programs. Take me there: fitnessDirectory.html',
            'sports': 'Sports directory: Explore sports activities and tournaments. Take me there: sportsDirectory.html',
            'wellness': 'Wellness directory: Discover wellness and health programs. Take me there: wellnessDirectory.html',
            'kids': 'Kids directory: Activities and programs for children. Take me there: kidsDirectory.html',
            'social': 'Social directory: Social events and community gatherings. Take me there: socialDirectory.html',
            'outdoor': 'Outdoor directory: Outdoor activities and adventures. Take me there: outdoorDirectory.html',
            'culinary': 'Culinary directory: Cooking classes and food-related events. Take me there: culinaryDirectory.html',
            'seasonal': 'Seasonal directory: Seasonal programs and special events. Take me there: seasonalDirectory.html'
        }
        
        suggestions = []
        for keyword, directory in directories.items():
            if keyword in query_lower:
                suggestions.append(directory)
        
        return suggestions

    def _search_activities(self, query):
        query_lower = query.lower()
        tokens = re.findall(r'\b[a-z]+\b', query_lower)
        stopwords = {'the', 'a', 'an', 'and', 'or', 'to', 'of', 'in', 'on', 'for', 'with', 'is', 'are', 'do', 'does', 'can', 'we', 'our', 'you', 'your', 'about', 'any', 'tell', 'me', 'please'}
        tokens = [t for t in tokens if t not in stopwords]

        if not tokens or (len(tokens) <= 2 and 'activity' in query_lower):
            return {'type': 'general', 'matches': []}

        matches = []
        for activity in self.activities:
            haystack = f"{activity['title']} {activity['description']} {activity['category']}".lower()
            score = sum(1 for t in tokens if t in haystack)
            if score > 0:
                matches.append((score, activity))

        matches.sort(key=lambda x: (x[0], 1 if x[1].get('category') != 'search' else 0), reverse=True)

        # Deduplicate same activity text showing up across "search" and category pages.
        deduped = []
        seen = set()
        for score, activity in matches:
            key = (activity['title'].strip().lower(), activity['description'].strip().lower())
            if key in seen:
                continue
            seen.add(key)
            deduped.append((score, activity))
            if len(deduped) >= 6:
                break

        return {'type': 'matches', 'matches': [m[1] for m in deduped]}

    def _extract_have_subject(self, query):
        query_lower = query.lower().strip()
        match = re.search(r'\bdo\s+you\s+have\s+(.+)$', query_lower)
        if not match:
            return None

        subject = match.group(1).strip(' ?.!')
        if not subject:
            return None

        subject = re.sub(r'\b(any|a|an|the|some)\b', ' ', subject)
        subject = re.sub(r'\s+', ' ', subject).strip()
        return subject or None

    def _search_have_matches(self, subject):
        subject_lower = subject.lower()
        subject_tokens = [
            t for t in re.findall(r'\b[a-z]+\b', subject_lower)
            if t not in {
                'class', 'classes', 'program', 'programs', 'event', 'events', 'service', 'services',
                'night', 'day', 'morning', 'evening', 'session', 'sessions', 'activity', 'activities'
            }
        ]

        def has_word_token(text, token):
            return re.search(r'\b' + re.escape(token) + r'\b', text) is not None

        activity_hits = []
        for activity in self.activities:
            title = activity['title'].lower()
            desc = activity['description'].lower()
            haystack = f"{title} {desc} {activity['category'].lower()}"

            score = 0
            if subject_lower in title:
                score += 6
            elif subject_lower in haystack:
                score += 4

            token_hits = sum(1 for t in subject_tokens if has_word_token(haystack, t))
            if token_hits:
                score += token_hits

            if score > 0:
                activity_hits.append((score, activity))

        activity_hits.sort(key=lambda x: (x[0], 1 if x[1].get('category') != 'search' else 0), reverse=True)

        deduped_activity = []
        seen = set()
        for score, activity in activity_hits:
            key = (activity['title'].strip().lower(), activity['description'].strip().lower())
            if key in seen:
                continue
            seen.add(key)
            deduped_activity.append(activity)
            if len(deduped_activity) >= 3:
                break

        event_hits = []
        for date, events_list in self.events.items():
            for event in events_list:
                event_lower = event.lower()
                score = 0
                if subject_lower in event_lower:
                    score += 5
                token_hits = sum(1 for t in subject_tokens if has_word_token(event_lower, t))
                if token_hits:
                    score += token_hits
                if score > 0:
                    event_hits.append((score, date, event))

        event_hits.sort(key=lambda x: x[0], reverse=True)
        deduped_events = []
        seen_event_text = set()
        for score, date, event in event_hits:
            key = event.lower()
            if key in seen_event_text:
                continue
            seen_event_text.add(key)
            deduped_events.append((date, event))
            if len(deduped_events) >= 2:
                break

        return deduped_activity, deduped_events
    
    def _retrieve_relevant_content(self, query, top_k=3):
        query_lower = query.lower()
        if any(word in query_lower for word in ['contact', 'phone', 'email', 'address', 'location', 'locate', 'where', 'reach', 'call']):
            return [{'content': self._extract_contact_info(query), 'filename': 'contact', 'type': 'contact'}]

        have_subject = self._extract_have_subject(query)
        if have_subject:
            activity_hits, event_hits = self._search_have_matches(have_subject)
            if activity_hits or event_hits:
                parts = []
                for activity in activity_hits:
                    desc = activity['description']
                    if desc:
                        parts.append(f"{activity['title']} - {desc} ({activity['category'].capitalize()})")
                    else:
                        parts.append(f"{activity['title']} ({activity['category'].capitalize()})")

                for date, event in event_hits:
                    parts.append(f"{date}: {event}")

                link_source = activity_hits[0].get('source') if activity_hits else None
                if link_source and link_source.endswith('.html'):
                    parts.append(f"Take me there: {link_source}")

                content = "HAVE_QUERY_MATCHES:" + have_subject + "||" + "||".join(parts)
                return [{'content': content, 'filename': 'directories', 'type': 'have_query'}]

            return [{'content': f"HAVE_QUERY_NONE:{have_subject}", 'filename': 'directories', 'type': 'have_query'}]

        date_key = self._parse_date_from_query(query)
        if date_key:
            events_on_date = self.events.get(date_key, [])
            topic_label = self._extract_event_topic_from_query(query_lower)
            if topic_label:
                events_on_date = self._filter_events_for_topic(events_on_date, topic_label)
            if events_on_date:
                content = "EVENTS_ON_DATE:" + date_key + "||" + "||".join(events_on_date)
            else:
                content = "EVENTS_ON_DATE:" + date_key + "||NONE"
            return [{'content': content, 'filename': 'calendar.js', 'type': 'event'}]

        if 'mission' in query_lower:
            if self.mission_text:
                return [{'content': self.mission_text, 'filename': 'aboutus.html', 'type': 'mission'}]

        if any(phrase in query_lower for phrase in ['how did you begin', 'where did we begin', 'how did we begin', 'origin story', 'how it started']):
            if self.origin_text:
                return [{'content': self.origin_text, 'filename': 'aboutus.html', 'type': 'origin'}]

        if any(word in query_lower for word in ['activity', 'activities', 'things to do', 'classes', 'programs', 'what do you offer', 'offer', 'offered', 'available', 'have', 'tell me about', 'basketball', 'pickleball', 'hiking', 'trail', 'tennis', 'soccer', 'swimming', 'yoga', 'fitness', 'outdoor', 'kids', 'culinary', 'wellness']):
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
                    link = None
                    for activity in activity_search['matches']:
                        desc = activity['description']
                        source = activity.get('source')
                        if not link and source and source.endswith('.html'):
                            link = source
                        if desc:
                            parts.append(f"{activity['title']} - {desc} ({activity['category'].capitalize()})")
                        else:
                            parts.append(f"{activity['title']} ({activity['category'].capitalize()})")
                    if link:
                        parts.append(f"Take me there: {link}")
                    content = "ACTIVITY_MATCHES:" + "||".join(parts)
                    return [{'content': content, 'filename': 'directories', 'type': 'activity_list'}]
        
        faq_answer = self._find_faq_match(query)
        if faq_answer:
            return [{'content': faq_answer, 'filename': 'aboutus.html', 'type': 'faq'}]
        
        if any(word in query_lower for word in ['event', 'schedule', 'when', 'time', 'class', 'activity']):
            upcoming_events = self._get_upcoming_events(query)
            if upcoming_events:
                event_content = "Here are some upcoming events: " + "; ".join(upcoming_events)
                return [{'content': event_content, 'filename': 'calendar.js', 'type': 'event'}]
        
        directory_suggestions = self._suggest_directories(query)
        if directory_suggestions:
            dir_content = "You might want to check out: " + ", ".join(directory_suggestions)
            return [{'content': dir_content, 'filename': 'directories', 'type': 'navigation'}]
        
        try:
            similarities = self.vectorizer.find_most_similar(query, top_k=top_k)
            
            results = []
            for idx, similarity_score in similarities:
                if similarity_score > 0.01:
                    metadata = self.document_metadata[idx]
                    content = self.documents[idx]
                    
                    results.append({
                        'content': content,
                        'similarity': similarity_score,
                        'filename': metadata['filename'],
                        'type': metadata.get('type', 'full'),
                        'metadata': metadata
                    })
            
            if not results:
                return [{'content': "LOW_CONFIDENCE", 'filename': 'low_confidence', 'type': 'fallback'}]
            
            return results
        except Exception as e:
            print(f"Error retrieving content: {e}")
            return [{'content': "I'm having trouble finding information right now. Please try again later.", 'filename': 'error', 'type': 'fallback'}]
    
    def ask(self, query):
        if not query or not query.strip():
            return "Please ask me a question about Mile High Movement community center!"
        
        original_query = query.strip()
        query = self._rewrite_event_followup_query(original_query)
        
        query_lower = query.lower()
        if query_lower in ['tell me more', 'more info', 'elaborate', 'expand', 'details'] and self.history:
            last = self.history[-1]
            return f"More about your previous question '{last['query']}': {last['response']}"
        
        retrieved_results = self._retrieve_relevant_content(query, top_k=3)
        
        combined_content = self.response_generator.combine_multiple_results(retrieved_results)
        
        response = self.response_generator.generate_response(query, combined_content)

        detected_topic = 'general'
        for result in retrieved_results:
            content = result.get('content', '') if isinstance(result, dict) else ''
            if isinstance(content, str) and content.startswith('EVENTS_ON_DATE:'):
                parts = content.replace('EVENTS_ON_DATE:', '').split('||')
                if parts and parts[0].strip():
                    self.last_event_date = parts[0].strip()
                detected_topic = 'event'
                break
        if detected_topic != 'event' and any(word in query_lower for word in ['event', 'events', 'schedule']):
            detected_topic = 'event'
        
        self.history.append({'query': original_query, 'resolved_query': query, 'response': response, 'topic': detected_topic})
        self.history = self.history[-5:]
        
        return response
    
    def get_events(self):
        return dict(sorted(self.events.items()))  # Sort by date

    def get_status(self):
        return {
            'documents_indexed': len(self.documents),
            'html_files_loaded': len(self.html_content),
            'events_loaded': len(self.events),
            'faqs_loaded': len(self.faqs),
            'activities_loaded': len(self.activities),
            'history_size': len(self.history)
        }
