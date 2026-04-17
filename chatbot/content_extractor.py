import re
import os
from html.parser import HTMLParser


class CustomHTMLParser(HTMLParser):
    
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.current_tag = None
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'head'}
        self.important_tags = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'title'}
        self.in_skip = False
        self.in_important = False
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag.lower()
        if self.current_tag in self.skip_tags:
            self.in_skip = True
        elif self.current_tag in self.important_tags:
            self.in_important = True
    
    def handle_endtag(self, tag):
        if tag.lower() in self.skip_tags:
            self.in_skip = False
        elif tag.lower() in self.important_tags:
            self.in_important = False
        self.current_tag = None
    
    def handle_data(self, data):
        if not self.in_skip and data.strip():
            clean_data = ' '.join(data.split())
            if clean_data:
                self.text_content.append(clean_data)

def extract_text_from_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        parser = CustomHTMLParser()
        parser.feed(html_content)
        
        full_text = ' '.join(parser.text_content)
        
        full_text = re.sub(r'\s+', ' ', full_text).strip()
        
        return full_text
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""

def extract_structured_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        structured = {
            'title': '',
            'headings': [],
            'paragraphs': [],
            'items': []
        }
        
        title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        if not title_match:
            title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
        if title_match:
            structured['title'] = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        
        heading_pattern = r'<h[1-6][^>]*>(.*?)</h[1-6]>'
        headings = re.findall(heading_pattern, html_content, re.IGNORECASE | re.DOTALL)
        structured['headings'] = [re.sub(r'<[^>]+>', '', h).strip() for h in headings if h.strip()]
        
        para_pattern = r'<p[^>]*>(.*?)</p>'
        paras = re.findall(para_pattern, html_content, re.IGNORECASE | re.DOTALL)
        structured['paragraphs'] = [re.sub(r'<[^>]+>', '', p).strip() for p in paras if p.strip()]
        
        event_title_pattern = r'<h[12][^>]*class="[^"]*eventTitle[^"]*"[^>]*>(.*?)</h[12]>'
        event_titles = re.findall(event_title_pattern, html_content, re.IGNORECASE | re.DOTALL)
        items = [re.sub(r'<[^>]+>', '', t).strip() for t in event_titles if t.strip()]

        li_pattern = r'<li[^>]*>(.*?)</li>'
        lis = re.findall(li_pattern, html_content, re.IGNORECASE | re.DOTALL)
        items.extend([re.sub(r'<[^>]+>', '', li).strip() for li in lis if li.strip()])
        structured['items'] = items
        
        return structured
    except Exception as e:
        print(f"Error extracting structured content from {file_path}: {e}")
        return {'title': '', 'headings': [], 'paragraphs': [], 'items': []}

def load_all_html_files(directory):
    html_files = {}
    skip_dirs = {'.git', 'node_modules', '__pycache__', 'chatbot'}

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for filename in files:
            if filename.endswith('.html'):
                file_path = os.path.join(root, filename)
                text_content = extract_text_from_html(file_path)
                structured_content = extract_structured_content(file_path)
                rel_path = os.path.relpath(file_path, directory)

                if text_content:
                    html_files[rel_path] = {
                        'text': text_content,
                        'structured': structured_content,
                        'filename': rel_path
                    }

    return html_files

