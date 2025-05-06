"""
Embedder module for the RAG service.

This module provides functionality to convert text chunks into vector embeddings
using either OpenAI embeddings or Hugging Face sentence transformers.
"""

import os
import logging
import numpy as np
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

DEFAULT_EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformer')  # 'openai' or 'sentence-transformer'
OPENAI_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-ada-002')
SENTENCE_TRANSFORMER_MODEL = os.getenv('SENTENCE_TRANSFORMER_MODEL', 'all-MiniLM-L6-v2')
EMBEDDING_DIMENSION = int(os.getenv('EMBEDDING_DIMENSION', '0'))  # 0 means auto-detect

class Embedder:
    """
    Class for converting text to vector embeddings.
    """
    
    def __init__(self, model_type: Optional[str] = None):
        """
        Initialize the embedder.
        
        Args:
            model_type: Type of embedding model to use ('openai' or 'sentence-transformer')
        """
        self.model_type = model_type or DEFAULT_EMBEDDING_MODEL
        self.model = None
        self.dimension = EMBEDDING_DIMENSION
        
        if self.model_type == 'openai':
            try:
                import openai
                openai.api_key = os.getenv('OPENAI_API_KEY')
                if not openai.api_key:
                    raise ValueError("OpenAI API key not found in environment variables")
                
                if self.dimension == 0:
                    if OPENAI_MODEL == 'text-embedding-ada-002':
                        self.dimension = 1536
                    else:
                        pass
                
                logger.info(f"Using OpenAI embedding model: {OPENAI_MODEL}")
            except ImportError:
                logger.warning("OpenAI package not installed. Falling back to sentence-transformer.")
                self.model_type = 'sentence-transformer'
        
        if self.model_type == 'sentence-transformer':
            self.model = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
            
            if self.dimension == 0:
                self.dimension = self.model.get_sentence_embedding_dimension()
            
            logger.info(f"Using Sentence Transformer model: {SENTENCE_TRANSFORMER_MODEL} with dimension {self.dimension}")
    
    def embed_text(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Convert text to vector embeddings.
        
        Args:
            text: Text or list of texts to embed
            
        Returns:
            Numpy array of embeddings
        """
        if isinstance(text, str):
            text = [text]
        
        if self.model_type == 'openai':
            return self._embed_with_openai(text)
        else:
            return self._embed_with_sentence_transformer(text)
    
    def _embed_with_openai(self, texts: List[str]) -> np.ndarray:
        """
        Embed text using OpenAI API.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            Numpy array of embeddings
        """
        import openai
        
        try:
            batch_size = 1000
            all_embeddings = []
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i+batch_size]
                
                response = openai.Embedding.create(
                    input=batch,
                    model=OPENAI_MODEL
                )
                
                batch_embeddings = [item["embedding"] for item in response["data"]]
                all_embeddings.extend(batch_embeddings)
            
            embeddings = np.array(all_embeddings, dtype=np.float32)
            
            if self.dimension == 0:
                self.dimension = embeddings.shape[1]
                logger.info(f"Auto-detected embedding dimension: {self.dimension}")
            
            return embeddings
            
        except Exception as e:
            logger.error(f"Error embedding text with OpenAI: {str(e)}")
            raise
    
    def _embed_with_sentence_transformer(self, texts: List[str]) -> np.ndarray:
        """
        Embed text using Sentence Transformer.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            Numpy array of embeddings
        """
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings.astype(np.float32)
        except Exception as e:
            logger.error(f"Error embedding text with Sentence Transformer: {str(e)}")
            raise
    
    def get_dimension(self) -> int:
        """
        Get the dimension of the embeddings.
        
        Returns:
            Embedding dimension
        """
        return self.dimension
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the embedding model.
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_type": self.model_type,
            "model_name": OPENAI_MODEL if self.model_type == 'openai' else SENTENCE_TRANSFORMER_MODEL,
            "dimension": self.dimension
        }


def get_embedder(model_type: Optional[str] = None) -> Embedder:
    """
    Factory function to get an embedder instance.
    
    Args:
        model_type: Type of embedding model to use ('openai' or 'sentence-transformer')
        
    Returns:
        Embedder instance
    """
    return Embedder(model_type)


if __name__ == "__main__":
    texts = [
        "This is a sample document for testing embeddings.",
        "Vector embeddings are useful for semantic search."
    ]
    
    print("Testing with default embedder:")
    embedder = get_embedder()
    embeddings = embedder.embed_text(texts)
    print(f"Generated {len(embeddings)} embeddings with dimension {embeddings.shape[1]}")
    print(f"Model info: {embedder.get_model_info()}")
    
    if os.getenv('OPENAI_API_KEY'):
        print("\nTesting with OpenAI embedder:")
        openai_embedder = get_embedder('openai')
        openai_embeddings = openai_embedder.embed_text(texts)
        print(f"Generated {len(openai_embeddings)} embeddings with dimension {openai_embeddings.shape[1]}")
        print(f"Model info: {openai_embedder.get_model_info()}")
