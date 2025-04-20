import os
import json
import requests

class LLMService:
    def __init__(self, model_id="mistralai/Mistral-7B-Instruct-v0.2"):
        """
        Initialize the LLM service using Hugging Face Inference API.
        
        Args:
            model_id (str): Model identifier on Hugging Face
        """
        self.model_id = model_id
        self.api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY', '')}",
            "Content-Type": "application/json"
        }
    
    def generate_response(self, prompt, max_length=250, temperature=0.7):
        """
        Generate a response from the LLM.
        
        Args:
            prompt (str): Input text prompt
            max_length (int): Maximum length of the generated response (capped at 250)
            temperature (float): Controls randomness in generation
            
        Returns:
            str: Generated text response or error message
        """
        try:
            # Ensure max_length doesn't exceed the model's limit
            max_length = min(max_length, 250)
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_length,
                    "temperature": temperature,
                    "top_p": 0.95,
                    "do_sample": True,
                }
            }
            
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                # Format might vary based on model, adjust as needed
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
                return str(result)
            else:
                return f"Error: API returned status code {response.status_code}. Message: {response.text}"
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_explanation(self, claim, facts, evidence_passages, verdict, temperature=None, max_length=None):
        """
        Generate an explanation for a paranormal claim analysis using the LLM.
        
        Args:
            claim (str): The paranormal claim text
            facts (dict): Extracted key facts from evidence
            evidence_passages (list): List of relevant evidence passages
            verdict (str): The verdict (Debunked, Unsupported, etc.)
            temperature (float, optional): Controls randomness in generation
            max_length (int, optional): Maximum length of the generated response
            
        Returns:
            str: Generated explanation
        """
        # Get temperature and max_length from Streamlit session state if available
        import streamlit as st
        if temperature is None and 'temperature' in st.session_state:
            temperature = st.session_state.temperature
        else:
            temperature = temperature or 0.5
            
        if max_length is None and 'max_length' in st.session_state:
            max_length = min(st.session_state.max_length, 250)  # Cap at 250 for API limit
        else:
            max_length = min(max_length or 250, 250)  # Cap at 250 for API limit
        
        # Format evidence passages for the prompt
        evidence_text = ""
        for i, passage in enumerate(evidence_passages[:3]):  # Limit to top 3 for prompt size
            evidence_text += f"Evidence {i+1} from {passage['source']}: {passage['text'][:300]}...\n\n"
        
        # Convert sets to lists for JSON serialization
        facts_json = dict(facts)
        if 'sources' in facts_json and isinstance(facts_json['sources'], set):
            facts_json['sources'] = list(facts_json['sources'])
        if 'domains' in facts_json and isinstance(facts_json['domains'], set):
            facts_json['domains'] = list(facts_json['domains'])
        
        # Create a prompt for the LLM
        prompt = f"""
        Task: Generate a detailed explanation for the analysis of a paranormal claim.
        
        Claim: "{claim}"
        
        Evidence summary:
        {evidence_text}
        
        Key facts:
        {json.dumps(facts_json, indent=2)}
        
        Verdict: {verdict}
        
        Please provide a thorough explanation for this verdict, referencing the evidence and key facts. 
        Maintain an objective, scientific tone. If debunked, explain why the claim contradicts evidence. 
        If unsupported, explain the lack of supporting evidence. If more research is needed, explain what 
        aspects require further investigation.
        
        Explanation:
        """
        
        # Generate the explanation
        explanation = self.generate_response(prompt, max_length=max_length, temperature=temperature)
        
        # Clean up the response if needed
        if "Explanation:" in explanation:
            explanation = explanation.split("Explanation:")[1].strip()
            
        return explanation