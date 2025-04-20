import streamlit as st
import os
import time
import io

from data_processor import DataProcessor
from embedding_engine import EmbeddingEngine
from rag_system import RAGSystem
from claim_analyzer import ClaimAnalyzer
from sample_data_generator import generate_sample_data

# Set page config
st.set_page_config(
    page_title="Pakhand Bhedi - Paranormal Debunking AI",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state for persistence across reruns
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.data_loaded = False
    st.session_state.embeddings_created = False
    st.session_state.claim_history = []
    st.session_state.current_verdict = None
    st.session_state.current_evidence = None
    st.session_state.current_claim = None
    st.session_state.current_explanation = None
    st.session_state.current_confidence = None
    st.session_state.domain_filter = "All"
    # LLM settings
    st.session_state.use_llm = True
    st.session_state.hf_api_key = os.getenv("HUGGINGFACE_API_KEY", "")
    st.session_state.selected_model = "google/flan-t5-large"  # Smaller model that works with free tier
    st.session_state.temperature = 0.7
    st.session_state.max_length = 500

# Initialize our system components
@st.cache_resource
def initialize_system():
    # Generate sample data first
    claims_data, myths_data = generate_sample_data()
    
    # Initialize all components
    data_processor = DataProcessor()
    embedding_engine = EmbeddingEngine()
    rag_system = RAGSystem(embedding_engine)
    
    # Initialize claim analyzer with LLM settings
    claim_analyzer = ClaimAnalyzer(use_llm=st.session_state.use_llm)
    
    # If using LLM, update the settings
    if st.session_state.use_llm and hasattr(claim_analyzer, 'llm_service'):
        # Update the model and settings if LLM service is available
        claim_analyzer.llm_service.model_id = st.session_state.selected_model
        # The API URL needs to be updated with the new model_id
        claim_analyzer.llm_service.api_url = f"https://api-inference.huggingface.co/models/{st.session_state.selected_model}"
        # Update API key in the headers
        claim_analyzer.llm_service.headers = {
            "Authorization": f"Bearer {st.session_state.hf_api_key}",
            "Content-Type": "application/json"
        }
    
    return {
        'data_processor': data_processor,
        'embedding_engine': embedding_engine,
        'rag_system': rag_system,
        'claim_analyzer': claim_analyzer,
        'claims_data': claims_data,
        'myths_data': myths_data
    }

# Main application function
def main():
    st.title("Pakhand Bhedi - Paranormal Debunking AI 🔍")
    st.subheader("Using evidence-based reasoning to analyze paranormal claims")
    
    # Initialize the system if not already done
    if not st.session_state.initialized:
        with st.spinner("Initializing the system..."):
            system = initialize_system()
            st.session_state.system = system
            st.session_state.initialized = True
    
    # Get system components
    system = st.session_state.system
    data_processor = system['data_processor']
    embedding_engine = system['embedding_engine']
    rag_system = system['rag_system']
    claim_analyzer = system['claim_analyzer']
    claims_data = system['claims_data']
    myths_data = system['myths_data']
    
    # Data processing and embedding section
    with st.sidebar:
        st.header("System Status")
        
        # Process data if not already done
        if not st.session_state.data_loaded:
            if st.button("Load & Process Data"):
                with st.spinner("Processing data..."):
                    processed_claims = data_processor.process_claims(claims_data)
                    processed_myths = data_processor.process_texts(myths_data)
                    st.session_state.processed_data = {
                        'claims': processed_claims,
                        'myths': processed_myths
                    }
                    st.session_state.data_loaded = True
                    st.success("Data processed successfully!")
        else:
            st.success("✅ Data loaded and processed")
        
        # Create embeddings if data is loaded but embeddings aren't created
        if st.session_state.data_loaded and not st.session_state.embeddings_created:
            if st.button("Create Embeddings"):
                with st.spinner("Creating embeddings and indexing..."):
                    processed_data = st.session_state.processed_data
                    embedding_engine.create_embeddings(processed_data['myths'])
                    st.session_state.embeddings_created = True
                    st.success("Embeddings created and indexed successfully!")
        elif st.session_state.embeddings_created:
            st.success("✅ Embeddings created and indexed")
            
        # Domain filter
        st.header("Filters")
        domain_options = ["All", "Ghost Myths", "UFO Encounters", "Astrology", "Supernatural Powers"]
        st.session_state.domain_filter = st.selectbox("Domain Filter", domain_options)
        
        # History of claims
        st.header("Claim History")
        if st.session_state.claim_history:
            for idx, claim_info in enumerate(st.session_state.claim_history):
                if st.button(f"{claim_info['claim'][:30]}... ({claim_info['verdict']})", key=f"history_{idx}"):
                    st.session_state.current_claim = claim_info['claim']
                    st.session_state.current_verdict = claim_info['verdict']
                    st.session_state.current_evidence = claim_info['evidence']
                    st.session_state.current_explanation = claim_info['explanation']
                    st.session_state.current_confidence = claim_info['confidence']
                    st.rerun()
        else:
            st.write("No claims analyzed yet.")
    
    # Main content area
    main_tabs = st.tabs(["Submit Claim", "About Pakhand Bhedi", "Settings"])
    
    with main_tabs[0]:
        st.header("Submit a Paranormal Claim for Analysis")
        
        # Check if system is ready for claim analysis
        system_ready = st.session_state.data_loaded and st.session_state.embeddings_created
        
        if not system_ready:
            st.warning("Please load data and create embeddings before submitting claims.")
        
        claim_input = st.text_area("Enter your paranormal claim:", 
                                   placeholder="Example: I saw a ghost that walked through walls last night at the old mansion.",
                                   disabled=not system_ready)
        
        col1, col2 = st.columns([1, 5])
        with col1:
            analyze_button = st.button("Analyze Claim", disabled=not system_ready or not claim_input)
        
        # Analyze button functionality
        if analyze_button and claim_input and system_ready:
            with st.spinner("Analyzing your claim..."):
                # Process the claim
                processed_claim = data_processor.process_claim_text(claim_input)
                
                # Filter by domain if needed
                domain_filter = None if st.session_state.domain_filter == "All" else st.session_state.domain_filter
                
                # Get evidence through RAG
                evidence_passages = rag_system.retrieve_evidence(processed_claim, k=5, domain_filter=domain_filter)
                
                # Analyze the claim against evidence
                verdict, explanation, confidence = claim_analyzer.analyze_claim(processed_claim, evidence_passages)
                
                # Store results in session state
                st.session_state.current_claim = claim_input
                st.session_state.current_verdict = verdict
                st.session_state.current_evidence = evidence_passages
                st.session_state.current_explanation = explanation
                st.session_state.current_confidence = confidence
                
                # Add to history
                claim_info = {
                    'claim': claim_input,
                    'verdict': verdict,
                    'evidence': evidence_passages,
                    'explanation': explanation,
                    'confidence': confidence
                }
                st.session_state.claim_history.append(claim_info)
        
        # Display results if available
        if st.session_state.current_verdict:
            st.markdown("---")
            st.header("Analysis Results")
            
            # Display claim
            st.subheader("Claim:")
            st.write(st.session_state.current_claim)
            
            # Display verdict with appropriate color
            verdict = st.session_state.current_verdict
            if verdict == "Debunked":
                st.markdown(f"<h3 style='color: red;'>Verdict: {verdict}</h3>", unsafe_allow_html=True)
            elif verdict == "Unsupported":
                st.markdown(f"<h3 style='color: orange;'>Verdict: {verdict}</h3>", unsafe_allow_html=True)
            else:  # "Requires Further Research"
                st.markdown(f"<h3 style='color: blue;'>Verdict: {verdict}</h3>", unsafe_allow_html=True)
            
            # Display explanation
            st.subheader("Explanation:")
            st.write(st.session_state.current_explanation)
            
            # Display confidence
            st.subheader("Confidence Level:")
            st.progress(st.session_state.current_confidence)
            st.write(f"{st.session_state.current_confidence:.2f} out of 1.0")
            
            # Display evidence
            st.subheader("Supporting Evidence:")
            for i, passage in enumerate(st.session_state.current_evidence):
                with st.expander(f"Evidence #{i+1} - Similarity: {passage['similarity']:.2f}"):
                    st.write(f"**Source:** {passage['source']}")
                    st.write(f"**Publication Date:** {passage['publication_date']}")
                    st.write(f"**Domain:** {passage['domain']}")
                    st.write("**Passage:**")
                    st.write(passage['text'])
    
    with main_tabs[1]:
        st.header("About Pakhand Bhedi")
        st.write("""
        **Pakhand Bhedi** is an AI-powered system designed to analyze and debunk paranormal claims using 
        evidence-based reasoning. The name "Pakhand Bhedi" roughly translates to "Exposer of False Practices" 
        in Hindi.
        
        ### How It Works
        
        1. **Data Processing**: We process a knowledge base of factual information and known myths.
        2. **Embeddings**: We convert text into numerical representations that capture meaning.
        3. **Retrieval-Augmented Generation (RAG)**: When you submit a claim, we find the most relevant evidence.
        4. **Analysis**: We compare your claim against the evidence to determine its validity.
        5. **Verdict**: We provide a verdict along with supporting evidence and explanation.
        
        ### Verdicts
        
        - **Debunked**: Strong evidence contradicts the claim.
        - **Unsupported**: No evidence supports the claim.
        - **Requires Further Research**: Some evidence exists, but it's inconclusive.
        
        ### Limitations
        
        This is an MVP version with a limited knowledge base. Results should be considered preliminary, 
        and claims may need further investigation by domain experts.
        """)
        
    with main_tabs[2]:
        st.header("Settings")
        
        # LLM Settings
        st.subheader("LLM Settings")
        st.markdown("""
        This application can use an open-source Large Language Model (LLM) to generate more detailed
        and nuanced explanations for paranormal claim analysis. The LLM is accessed through the 
        Hugging Face Inference API, which requires an API key.
        """)
        
        # Toggle for using LLM
        use_llm = st.checkbox("Use LLM for Explanations", value=st.session_state.use_llm)
        if use_llm != st.session_state.use_llm:
            st.session_state.use_llm = use_llm
            # Reset the system to apply the change
            st.session_state.initialized = False
            st.rerun()
        
        # API Key input
        api_key = st.text_input(
            "Hugging Face API Key", 
            value=st.session_state.hf_api_key,
            type="password",
            help="Enter your Hugging Face API key to enable the LLM feature. You can get a free key at huggingface.co"
        )
        
        if api_key != st.session_state.hf_api_key:
            st.session_state.hf_api_key = api_key
            # Set environment variable
            os.environ["HUGGINGFACE_API_KEY"] = api_key
            # Reset the system to apply the change
            st.session_state.initialized = False
            st.rerun()
            
        # Model selection
        model_options = [
            "google/flan-t5-large",
            "google/flan-t5-base",
            "facebook/bart-large-cnn"
        ]
        
        selected_model = st.selectbox(
            "LLM Model", 
            model_options,
            index=model_options.index(st.session_state.selected_model) if st.session_state.selected_model in model_options else 0,
            help="Select which model to use for generating explanations. Different models have different strengths."
        )
        
        if selected_model != st.session_state.selected_model:
            st.session_state.selected_model = selected_model
            # Reset the system to apply the change
            st.session_state.initialized = False
            st.rerun()
        
        # Other settings
        st.subheader("Advanced Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            temperature = st.slider(
                "Temperature", 
                min_value=0.1, 
                max_value=1.0, 
                value=st.session_state.temperature, 
                step=0.1,
                help="Controls randomness in generation. Higher values produce more creative responses."
            )
            
            if temperature != st.session_state.temperature:
                st.session_state.temperature = temperature
                # No need to reset system here as this can be applied dynamically
            
        with col2:
            max_length = st.slider(
                "Maximum Length", 
                min_value=50, 
                max_value=250,  # Limited to 250 due to model constraints
                value=min(st.session_state.max_length, 250), 
                step=25,
                help="Maximum length of generated explanations in tokens (limited to 250 for API compatibility)."
            )
            
            if max_length != st.session_state.max_length:
                st.session_state.max_length = max_length
                # No need to reset system here as this can be applied dynamically
            
        st.markdown("---")
        st.info("Changes to settings will take effect after the system resets. If you've entered an API key, you may need to reload data and recreate embeddings in the sidebar.")

if __name__ == "__main__":
    main()
