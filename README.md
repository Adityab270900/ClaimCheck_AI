# Pakhand Bhedi - Paranormal Debunking AI

Pakhand Bhedi is an AI-powered system designed to analyze and debunk paranormal claims using evidence-based reasoning. The name "Pakhand Bhedi" roughly translates to "Exposer of False Practices" in Hindi.

## Features

- **Evidence-Based Analysis**: Uses a knowledge base of factual information to evaluate paranormal claims
- **Retrieval-Augmented Generation (RAG)**: Finds the most relevant evidence for each claim
- **LLM Integration**: Optional integration with Hugging Face models for enhanced explanations
- **Verdict Classification**: Provides clear verdicts (Debunked, Unsupported, Requires Further Research)
- **Confidence Scoring**: Indicates the reliability of analysis results
- **Domain Filtering**: Filter evidence by specific paranormal domains

## How It Works

1. **Data Processing**: Processes a knowledge base of factual information and known myths
2. **Embeddings**: Converts text into numerical representations that capture meaning
3. **Retrieval**: When you submit a claim, it finds the most relevant evidence
4. **Analysis**: Compares your claim against the evidence to determine its validity
5. **Explanation**: Provides a detailed explanation of the verdict with supporting evidence

## Getting Started

### Prerequisites

- Python 3.8+
- Streamlit
- Requests

### Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/pakhand-bhedi.git
cd pakhand-bhedi
```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Run the application:
```
streamlit run app.py
```

### Configuration

For enhanced explanation capabilities, you can use the Hugging Face Inference API:

1. Create a free account at [Hugging Face](https://huggingface.co/)
2. Generate an API key in your account settings
3. Enter the API key in the Settings tab of the application

## Limitations

This is an MVP version with a limited knowledge base. Results should be considered preliminary, and claims may need further investigation by domain experts.

## Sample Claims to Try

- "I saw a ghost that walked through walls last night at the old mansion."
- "UFOs were spotted over the city last week with flashing lights that no airplane could make."
- "When Mercury is in retrograde, electronic devices malfunction more frequently."
- "I can bend spoons with my mind through telekinesis."
- "The Bermuda Triangle causes ships and planes to mysteriously disappear."
- "Are goat sacrifices sacred and do they have supernatural powers?"

## License

This project is licensed under the MIT License - see the LICENSE file for details.