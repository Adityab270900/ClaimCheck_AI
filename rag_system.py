import random
from collections import Counter

class RAGSystem:
    def __init__(self, embedding_engine):
        """
        Initialize the RAG system with an embedding engine.
        
        Args:
            embedding_engine (EmbeddingEngine): The embedding engine for vector search
        """
        self.embedding_engine = embedding_engine
    
    def retrieve_evidence(self, claim_text, k=5, domain_filter=None):
        """
        Retrieve evidence passages for the given claim.
        
        Args:
            claim_text (str): The processed claim text
            k (int): Number of passages to retrieve
            domain_filter (str, optional): Domain to filter results by
            
        Returns:
            list: List of dictionaries with passage info and similarity scores
        """
        # Get embedding for the claim
        claim_embedding = self.embedding_engine.get_embedding(claim_text)
        
        # Retrieve similar passages
        evidence_passages = self.embedding_engine.search(
            claim_embedding, 
            k=k,
            domain_filter=domain_filter
        )
        
        return evidence_passages
    
    def bootstrap_retrieval(self, claim_text, k=5, num_runs=3, domain_filter=None):
        """
        Run multiple retrievals with different parameters to assess stability.
        
        Args:
            claim_text (str): The processed claim text
            k (int): Number of passages to retrieve per run
            num_runs (int): Number of retrieval runs
            domain_filter (str, optional): Domain to filter results by
            
        Returns:
            dict: Dictionary with multiple retrieval results
        """
        # This is a simplified version - in a real implementation, you might:
        # - Use different embedding models
        # - Apply different preprocessing steps
        # - Use different k values
        # - Add random variations to the query
        
        results = []
        
        # Get base embedding for the claim
        base_embedding = self.embedding_engine.get_embedding(claim_text)
        
        for i in range(num_runs):
            # Modify the keywords for each run (except first)
            if i == 0:
                claim_embedding = base_embedding
            else:
                # For subsequent runs, randomly modify the keyword frequencies
                modified_embedding = Counter()
                for word, count in base_embedding.items():
                    # Apply small random changes to frequencies
                    modified_count = max(1, count + random.randint(-1, 1))
                    modified_embedding[word] = modified_count
                    
                # Add a small chance of including a few random new keywords
                if random.random() < 0.3:  # 30% chance
                    for j in range(random.randint(1, 3)):  # Add 1-3 random words
                        random_word = f"random_term_{j}_{i}"
                        modified_embedding[random_word] = 1
                
                claim_embedding = modified_embedding
            
            # Retrieve similar passages
            evidence_passages = self.embedding_engine.search(
                claim_embedding, 
                k=k,
                domain_filter=domain_filter
            )
            
            results.append({
                'run_id': i,
                'passages': evidence_passages
            })
        
        return results
