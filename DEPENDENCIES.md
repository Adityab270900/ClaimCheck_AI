# Dependencies

This project requires the following packages:

- streamlit>=1.22.0
- requests>=2.28.0

To install these packages in your environment, you can run:

```bash
pip install streamlit requests
```

## Hugging Face API Access

For LLM-enhanced explanations, the application requires:

1. A Hugging Face account
2. An API key from Hugging Face
3. The API key entered in the application's Settings tab

The application uses the following models:
- google/flan-t5-large (default)
- google/flan-t5-base
- facebook/bart-large-cnn