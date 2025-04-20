import re
import string
import random
from datetime import datetime, timedelta

def clean_html(text):
    """
    Remove HTML tags from text.
    
    Args:
        text (str): Text containing HTML
        
    Returns:
        str: Text with HTML removed
    """
    return re.sub(r'<.*?>', '', text)

def normalize_text(text):
    """
    Normalize text by cleaning and standardizing.
    
    Args:
        text (str): Text to normalize
        
    Returns:
        str: Normalized text
    """
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Normalize punctuation
    text = text.translate(str.maketrans('', '', string.punctuation + '""'''))
    
    # Strip whitespace
    text = text.strip()
    
    return text

def calculate_confidence(similarities):
    """
    Calculate confidence score from similarity values.
    
    Args:
        similarities (list): List of similarity scores
        
    Returns:
        float: Confidence score (0-1)
    """
    if not similarities:
        return 0.0
    
    # Weight higher similarities more
    weighted_sum = sum(s ** 2 for s in similarities)
    weighted_count = sum(s for s in similarities)
    
    if weighted_count == 0:
        return 0.0
    
    # Normalize to 0-1
    confidence = min(1.0, weighted_sum / (len(similarities) * weighted_count))
    
    return confidence

def format_date(date_str):
    """
    Format date string consistently.
    
    Args:
        date_str (str): Date string
        
    Returns:
        str: Formatted date string
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str

def truncate_text(text, max_length=100):
    """
    Truncate text to specified length with ellipsis.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."
