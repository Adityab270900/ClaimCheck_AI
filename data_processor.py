import re
import string
import json
from io import StringIO
from collections import defaultdict

class DataProcessor:
    def __init__(self):
        """Initialize the data processor."""
        # No initialization needed
    
    def clean_text(self, text):
        """
        Clean text by removing HTML, normalizing punctuation, and lowercasing.
        
        Args:
            text (str): The text to clean
            
        Returns:
            str: Cleaned text
        """
        if not isinstance(text, str):
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Normalize punctuation
        text = text.translate(str.maketrans('', '', string.punctuation + '""'''))
        
        # Convert to lowercase
        text = text.lower()
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def segment_text(self, text, max_length=300):
        """
        Segment text into passages of approximately max_length words.
        
        Args:
            text (str): The text to segment
            max_length (int): Target maximum length of each passage in words
            
        Returns:
            list: List of text passages
        """
        if not text:
            return []
        
        # Simple sentence splitting using periods, question marks and exclamation points
        # This is a basic replacement for NLTK's sent_tokenize
        text = text.replace('!', '.').replace('?', '.')
        sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
        
        passages = []
        current_passage = []
        current_length = 0
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            
            # If adding this sentence would exceed max_length
            if current_length + sentence_words > max_length and current_length > 0:
                # Save current passage and start a new one
                passages.append(' '.join(current_passage))
                current_passage = [sentence]
                current_length = sentence_words
            else:
                # Add sentence to current passage
                current_passage.append(sentence)
                current_length += sentence_words
        
        # Add the last passage if it exists
        if current_passage:
            passages.append(' '.join(current_passage))
        
        return passages
    
    def process_claim_text(self, claim_text):
        """
        Process a single claim text.
        
        Args:
            claim_text (str): The claim text to process
            
        Returns:
            str: Processed claim text
        """
        return self.clean_text(claim_text)
    
    def process_claims(self, claims_data):
        """
        Process the claims dataset.
        
        Args:
            claims_data (list): List of dictionaries containing claims
            
        Returns:
            list: List of dictionaries with processed claim data
        """
        # Create a new list for processed claims
        processed_claims = []
        
        # Process each claim
        for claim in claims_data:
            processed_claim = claim.copy()
            processed_claim['processed_text'] = self.clean_text(claim.get('claim_text', ''))
            processed_claims.append(processed_claim)
        
        return processed_claims
    
    def process_texts(self, myths_data):
        """
        Process the texts dataset and segment into passages.
        
        Args:
            myths_data (list): List of dictionaries containing text documents
            
        Returns:
            list: List of dictionaries with processed passages and metadata
        """
        processed_passages = []
        
        for doc in myths_data:
            # Clean the text
            cleaned_text = self.clean_text(doc.get('text', ''))
            
            # Segment into passages
            passages = self.segment_text(cleaned_text)
            
            # Store each passage with its metadata
            for i, passage in enumerate(passages):
                processed_passages.append({
                    'text': passage,
                    'source': doc.get('source', 'unknown'),
                    'source_id': doc.get('source_id', f'doc_{i}'),
                    'publication_date': doc.get('publication_date', ''),
                    'domain': doc.get('domain', 'unknown'),
                    'passage_id': f"{doc.get('source_id', f'doc_{i}')}_{i}"
                })
        
        return processed_passages
