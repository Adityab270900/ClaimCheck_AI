import math
import re
from collections import Counter

class EmbeddingEngine:
    def __init__(self, model_name=None):
        """
        Initialize the embedding engine using a simple keyword-based approach.
        
        Args:
            model_name (str, optional): Ignored, kept for compatibility
        """
        self.passages = []
        self.keywords = {}  # Will store keyword frequencies for each passage
    
    def _extract_keywords(self, text):
        """
        Extract keywords from text with simple tokenization.
        
        Args:
            text (str): Text to extract keywords from
            
        Returns:
            Counter: Counter of keywords and their frequencies
        """
        # Convert to lowercase and replace non-alphanumeric with spaces
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # Split into tokens
        tokens = text.split()
        
        # Filter stop words (common words that don't add much meaning)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 
                      'were', 'in', 'to', 'of', 'for', 'with', 'by', 'at', 'on', 
                      'from', 'that', 'this', 'these', 'those', 'it', 'its', 'as', 
                      'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 
                      'did', 'will', 'would', 'shall', 'should', 'can', 'could', 
                      'may', 'might', 'must', 'their', 'they', 'them', 'he', 'she', 
                      'him', 'her', 'his', 'hers', 'i', 'me', 'my', 'mine', 'we', 
                      'us', 'our', 'ours', 'you', 'your', 'yours', 'not'}
        
        filtered_tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
        
        # Count frequencies
        return Counter(filtered_tokens)
    
    def create_embeddings(self, passages):
        """
        Process passages and extract keywords for each.
        
        Args:
            passages (list): List of dictionaries containing passage text and metadata
            
        Returns:
            bool: True if successful
        """
        # Store passages for later retrieval
        self.passages = passages
        
        # Process each passage to extract keywords
        for i, passage in enumerate(passages):
            keywords = self._extract_keywords(passage['text'])
            self.keywords[i] = keywords
        
        return True
    
    def get_embedding(self, text):
        """
        Extract keywords from query text.
        
        Args:
            text (str): Text to embed
            
        Returns:
            Counter: Keyword frequencies
        """
        # Extract keywords from the query text
        return self._extract_keywords(text)
    
    def search(self, query_keywords, k=5, domain_filter=None):
        """
        Search for similar passages using keyword matching.
        
        Args:
            query_keywords (Counter): Query keyword frequencies
            k (int): Number of results to return
            domain_filter (str, optional): Domain to filter results by
            
        Returns:
            list: List of dictionaries with passage info and similarity scores
        """
        if not self.keywords:
            raise ValueError("Keywords not created. Call create_embeddings first.")
        
        # Calculate similarity scores using dot product of term frequencies
        similarity_scores = []
        for idx, passage_keywords in self.keywords.items():
            score = 0
            # Calculate dot product
            for word, query_count in query_keywords.items():
                passage_count = passage_keywords.get(word, 0)
                score += query_count * passage_count
            
            # Normalize by document lengths using cosine similarity formula
            query_magnitude = math.sqrt(sum(c*c for c in query_keywords.values()))
            passage_magnitude = math.sqrt(sum(c*c for c in passage_keywords.values()))
            
            # Avoid division by zero
            magnitude_product = query_magnitude * passage_magnitude
            if magnitude_product > 0:
                score = score / magnitude_product
            else:
                score = 0
                
            similarity_scores.append((idx, score))
        
        # Sort by similarity (descending)
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Process results
        results = []
        for idx, similarity in similarity_scores:
            passage = self.passages[idx]
            
            # Filter by domain if specified
            if domain_filter and passage['domain'] != domain_filter:
                continue
            
            results.append({
                **passage,
                'similarity': similarity
            })
            
            # Stop once we have enough results after filtering
            if len(results) >= k:
                break
        
        return results
