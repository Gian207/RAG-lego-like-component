# main.py

import sys
import os
import yaml

# Add the RAG_modules directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'RAG_modules'))

from slitting import Slitting
from embedding import Embedding
from retrieval import Retrieval

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    # Load configuration
    config = load_config(os.path.join('RAG_modules', 'config.yaml'))
    
    text = "Your long text goes here..."
    
    # Initialize components with configuration
    slitting_component = Slitting(config)
    embedding_component = Embedding(config)
    retrieval_component = Retrieval(config)
    
    # Process the text through the components
    chunks = slitting_component.process(text)
    embeddings = embedding_component.process(chunks)
    top_k_embeddings = retrieval_component.process(embeddings)
    
    # Continue processing with other components...
    
    print(top_k_embeddings)

if __name__ == "__main__":
    main()