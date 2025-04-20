import re
from collections import Counter
from llm_service import LLMService

class ClaimAnalyzer:
    def __init__(self, use_llm=True):
        """
        Initialize the claim analyzer.
        
        Args:
            use_llm (bool): Whether to use LLM for generating explanations
        """
        self.confidence_threshold_high = 0.7
        self.confidence_threshold_medium = 0.5
        
        # Keywords that might indicate paranormal claims
        self.paranormal_keywords = [
            'ghost', 'spirit', 'haunted', 'supernatural', 'apparition',
            'ufo', 'alien', 'extraterrestrial', 'abduction', 'conspiracy',
            'psychic', 'telepathy', 'telekinesis', 'esp', 'clairvoyance',
            'astrology', 'horoscope', 'zodiac', 'star sign', 'alignment',
            'magic', 'miracle', 'unexplained', 'mysterious', 'paranormal'
        ]
        
        # Common debunking terms
        self.debunking_keywords = [
            'debunked', 'disproven', 'false', 'hoax', 'myth',
            'scientific explanation', 'natural phenomenon', 'optical illusion',
            'misidentification', 'pareidolia', 'confirmation bias',
            'hallucination', 'fabricated', 'no evidence', 'anecdotal'
        ]
        
        # Initialize LLM service if enabled
        self.use_llm = use_llm
        if use_llm:
            try:
                self.llm_service = LLMService()
            except Exception as e:
                print(f"Warning: Could not initialize LLM service: {e}")
                self.use_llm = False
    
    def extract_key_facts(self, passages):
        """
        Extract key facts from evidence passages.
        
        Args:
            passages (list): List of evidence passage dictionaries
            
        Returns:
            dict: Dictionary of extracted facts
        """
        facts = {
            'contradictions': [],
            'supporting_facts': [],
            'relevant_terms': Counter(),
            'sources': set(),
            'domains': set()
        }
        
        for passage in passages:
            text = passage['text']
            source = passage['source']
            domain = passage['domain']
            similarity = passage['similarity']
            
            # Add source and domain
            facts['sources'].add(source)
            facts['domains'].add(domain)
            
            # Check for contradictory statements
            for keyword in self.debunking_keywords:
                if keyword in text:
                    facts['contradictions'].append({
                        'text': text,
                        'source': source,
                        'keyword': keyword,
                        'similarity': similarity
                    })
            
            # Extract potentially relevant terms
            for keyword in self.paranormal_keywords:
                if keyword in text:
                    facts['relevant_terms'][keyword] += 1
            
            # If passage has high similarity, consider it supporting
            if similarity > self.confidence_threshold_high:
                facts['supporting_facts'].append({
                    'text': text,
                    'source': source,
                    'similarity': similarity
                })
        
        return facts
    
    def analyze_claim(self, claim_text, evidence_passages):
        """
        Analyze a claim against evidence passages.
        
        Args:
            claim_text (str): The processed claim text
            evidence_passages (list): List of retrieved evidence passages
            
        Returns:
            tuple: (verdict, explanation, confidence)
        """
        # Check if we have enough evidence
        if not evidence_passages:
            return "Requires Further Research", "No relevant evidence found.", 0.3
        
        # Extract facts from evidence
        facts = self.extract_key_facts(evidence_passages)
        
        # Calculate overall confidence based on similarity scores
        similarities = [p['similarity'] for p in evidence_passages]
        avg_similarity = sum(similarities) / len(similarities) if similarities else 0
        max_similarity = max(similarities) if similarities else 0
        
        # Initialize verdict and confidence
        verdict = "Requires Further Research"
        confidence = avg_similarity
        
        # Determine verdict based on facts
        if facts['contradictions'] and max_similarity > self.confidence_threshold_high:
            verdict = "Debunked"
            confidence = max(confidence, max_similarity)
        elif not facts['supporting_facts'] and avg_similarity > self.confidence_threshold_medium:
            verdict = "Unsupported"
            confidence = avg_similarity
        
        # Generate explanation
        explanation = self._generate_explanation(claim_text, verdict, facts, evidence_passages)
        
        return verdict, explanation, confidence
    
    def _generate_explanation(self, claim_text, verdict, facts, evidence_passages):
        """
        Generate an explanation for the verdict.
        
        Args:
            claim_text (str): The claim text
            verdict (str): The verdict
            facts (dict): Extracted facts
            evidence_passages (list): The evidence passages
            
        Returns:
            str: Generated explanation
        """
        # Try to use LLM for explanation if available
        if self.use_llm:
            try:
                return self.llm_service.generate_explanation(claim_text, facts, evidence_passages, verdict)
            except Exception as e:
                print(f"Warning: LLM generation failed: {e}. Falling back to rule-based explanation.")
                # If LLM fails, fall back to rule-based explanation
                self.use_llm = False
        
        # Rule-based explanation generation (fallback)
        explanation = ""
        
        if verdict == "Debunked":
            explanation = f"The claim has been debunked based on evidence from {len(facts['sources'])} sources. "
            
            # Add contradiction details
            if facts['contradictions']:
                explanation += "Specific contradictions include: "
                for i, contradiction in enumerate(facts['contradictions'][:3]):  # Limit to top 3
                    explanation += f"\n- {contradiction['source']} states: '{contradiction['text'][:100]}...'"
                    
            # Add highest similarity passage
            top_passage = max(evidence_passages, key=lambda x: x['similarity'])
            explanation += f"\n\nStrongest evidence (similarity: {top_passage['similarity']:.2f}) from {top_passage['source']}: '{top_passage['text'][:150]}...'"
                
        elif verdict == "Unsupported":
            explanation = f"The claim lacks supporting evidence. "
            
            # Add details on what was searched
            explanation += f"We searched across {len(facts['domains'])} domains and {len(facts['sources'])} sources, but found no direct support for this claim. "
            
            # Add most relevant passage
            top_passage = max(evidence_passages, key=lambda x: x['similarity'])
            explanation += f"\n\nMost relevant information (similarity: {top_passage['similarity']:.2f}) from {top_passage['source']}: '{top_passage['text'][:150]}...'"
            
        else:  # "Requires Further Research"
            explanation = "The evidence is inconclusive. "
            
            if facts['relevant_terms']:
                explanation += f"Related concepts found in our knowledge base include: {', '.join(k for k, v in facts['relevant_terms'].most_common(5))}. "
            
            explanation += f"\nWhile we found {len(evidence_passages)} potentially relevant passages, none provided definitive confirmation or refutation of the claim. "
            
            # Add most similar passage
            top_passage = max(evidence_passages, key=lambda x: x['similarity'])
            explanation += f"\n\nMost relevant information (similarity: {top_passage['similarity']:.2f}) from {top_passage['source']}: '{top_passage['text'][:150]}...'"
            
            explanation += "\n\nThis claim would benefit from further investigation by domain experts."
        
        return explanation
