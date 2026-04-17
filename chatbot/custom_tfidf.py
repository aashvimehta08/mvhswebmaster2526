import re
import math
from collections import Counter, defaultdict
import nltk
from nltk.stem import WordNetLemmatizer

def _wordnet_available():
    try:
        nltk.data.find('corpora/wordnet')
        return True
    except LookupError:
        try:
            nltk.data.find('corpora/wordnet.zip')
            return True
        except LookupError:
            return False


if _wordnet_available():
    try:
        lemmatizer = WordNetLemmatizer()
        lemmatizer.lemmatize('test')
    except Exception:
        lemmatizer = None
else:
    lemmatizer = None

if lemmatizer is None:
    class _NoOpLemmatizer:
        def lemmatize(self, token):
            return token
    lemmatizer = _NoOpLemmatizer()

def tokenize(text):
    text = text.lower()
    tokens = re.findall(r'\b[a-z]+\b', text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens

def remove_stopwords(tokens):
    stopwords = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
        'to', 'was', 'were', 'will', 'with', 'the', 'this', 'but', 'they',
        'have', 'had', 'what', 'said', 'each', 'which', 'their', 'if',
        'up', 'out', 'many', 'then', 'them', 'these', 'so', 'some', 'her',
        'would', 'make', 'like', 'him', 'time', 'has', 'look', 'two',
        'more', 'write', 'go', 'see', 'number', 'no', 'way', 'could',
        'people', 'my', 'than', 'first', 'water', 'been', 'call', 'who',
        'oil', 'sit', 'now', 'find', 'down', 'day', 'did', 'get', 'come',
        'made', 'may', 'part', 'i', 'you', 'we', 'she', 'do', 'can'
    }
    return [token for token in tokens if token not in stopwords and len(token) > 2]

def compute_tf(term, document_tokens):
    if len(document_tokens) == 0:
        return 0
    return document_tokens.count(term) / len(document_tokens)

def compute_idf(term, all_documents):
    doc_count = sum(1 for doc in all_documents if term in doc)
    if doc_count == 0:
        return 0
    return math.log(len(all_documents) / doc_count)

class CustomTFIDFVectorizer:
    
    def __init__(self):
        self.vocabulary = {}
        self.idf_values = {}
        self.documents = []
        self.document_vectors = []
        
    def fit(self, documents):
        processed_docs = []
        for doc in documents:
            tokens = tokenize(doc)
            tokens = remove_stopwords(tokens)
            processed_docs.append(tokens)
        
        self.documents = processed_docs
        
        all_terms = set()
        for tokens in processed_docs:
            all_terms.update(tokens)
        
        self.vocabulary = {term: idx for idx, term in enumerate(sorted(all_terms))}
        
        self.idf_values = {}
        for term in self.vocabulary:
            self.idf_values[term] = compute_idf(term, processed_docs)
        
        self.document_vectors = []
        for tokens in processed_docs:
            vector = [0.0] * len(self.vocabulary)
            for term in tokens:
                if term in self.vocabulary:
                    tf = compute_tf(term, tokens)
                    idf = self.idf_values[term]
                    vector[self.vocabulary[term]] = tf * idf
            self.document_vectors.append(vector)
        
        return self
    
    def transform(self, query_text):
        tokens = tokenize(query_text)
        tokens = remove_stopwords(tokens)
        
        vector = [0.0] * len(self.vocabulary)
        for term in tokens:
            if term in self.vocabulary:
                tf = 1.0 if term in tokens else 0.0
                idf = self.idf_values.get(term, 0)
                vector[self.vocabulary[term]] = tf * idf
        
        return vector
    
    def cosine_similarity(self, vec1, vec2):
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(a * a for a in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def find_most_similar(self, query_text, top_k=3):
        query_vector = self.transform(query_text)
        
        similarities = []
        for idx, doc_vector in enumerate(self.document_vectors):
            similarity = self.cosine_similarity(query_vector, doc_vector)
            similarities.append((idx, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
