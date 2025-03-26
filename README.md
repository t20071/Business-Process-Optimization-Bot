# Business Process AI

Business Process AI is a Streamlit-based application that allows users to upload business process documents and interact with an AI-powered chatbot to analyze and optimize their current processes.

## Features
- Upload business process documents in PDF or DOCX format.
- Extract text from uploaded files.
- Generate text embeddings using Hugging Face embeddings.
- Store and retrieve document chunks using FAISS vector storage.
- Conversational AI interaction using OpenAI's GPT-3.5-turbo model.
- Memory-enabled chat history for context-aware responses.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Pip

### Setup

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Set up the environment variables:
   Create a `.env` file and add your OpenAI API key:
   ```sh
   OPENAI_KEY= "openai_api_key" 
   ```

## Usage
Run the Streamlit application:
```sh
streamlit run app.py
```

## How It Works
1. Upload one or more business process documents.
2. The text is extracted and split into chunks.
3. Text embeddings are generated and stored in a FAISS vector store.
4. A conversational AI model is initialized with memory.
5. Users can chat with the AI to analyze and optimize business processes.

## File Structure
```
📂 business-process-ai
│-- app.py                 # Main application script
│-- requirements.txt       # Required Python packages
│-- .env                   # Environment variables
│-- README.md              # Documentation
```

## Dependencies
- `streamlit`
- `PyPDF2`
- `docx`
- `langchain`
- `faiss-cpu`
- `huggingface-hub`
- `streamlit-chat`
- `python-dotenv`





