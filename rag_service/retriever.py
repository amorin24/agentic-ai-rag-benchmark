"""
Retriever module for the RAG service.

This module provides functionality to store and search vectorized document chunks
using FAISS for efficient similarity search.
"""

import os
import json
import time
import logging
import numpy as np
import faiss
from typing import List, Dict, Any, Optional, Union, Tuple
from pathlib import Path
from dotenv import load_dotenv

from rag_service.embedder import get_embedder

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

VECTOR_DIR = Path(os.getenv('VECTOR_DIR', 'data/vectors'))
PROCESSED_DIR = Path(os.getenv('PROCESSED_DOCS_DIR', 'data/processed'))
DEFAULT_TOP_K = int(os.getenv('DEFAULT_TOP_K', '5'))

VECTOR_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

class Retriever:
    """
    Class for storing and searching vectorized document chunks using FAISS.
    """
    
    def __init__(self, index_name: str = "default", embedding_model: Optional[str] = None):
        """
        Initialize the retriever.
        
        Args:
            index_name: Name of the FAISS index
            embedding_model: Type of embedding model to use ('openai' or 'sentence-transformer')
        """
        self.index_name = index_name
        self.index_path = VECTOR_DIR / f"{index_name}.index"
        self.metadata_path = VECTOR_DIR / f"{index_name}.json"
        
        self.embedder = get_embedder(embedding_model)
        self.embedding_dim = self.embedder.get_dimension()
        
        self.index = None
        self.doc_ids = []
        self.metadata = []
        
        if self.index_path.exists() and self.metadata_path.exists():
            self.load_index()
        else:
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            logger.info(f"Created new FAISS index with dimension {self.embedding_dim}")
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> int:
        """
        Add documents to the index.
        
        Args:
            documents: List of document dictionaries with 'id', 'chunks', and 'metadata'
            
        Returns:
            Number of chunks added to the index
        """
        if not documents:
            return 0
        
        total_chunks = 0
        
        for doc in documents:
            doc_id = doc.get('id')
            chunks = doc.get('chunks', [])
            doc_metadata = doc.get('metadata', {})
            
            if not chunks:
                logger.warning(f"Document {doc_id} has no chunks, skipping")
                continue
            
            embeddings = self.embedder.embed_text(chunks)
            
            self.index.add(embeddings)
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_id}_{i}"
                self.doc_ids.append(chunk_id)
                
                chunk_metadata = doc_metadata.copy()
                chunk_metadata['doc_id'] = doc_id
                chunk_metadata['chunk_index'] = i
                chunk_metadata['chunk_text'] = chunk
                chunk_metadata['added_at'] = time.time()
                
                self.metadata.append(chunk_metadata)
            
            total_chunks += len(chunks)
            logger.info(f"Added document {doc_id} with {len(chunks)} chunks to index")
        
        self.save_index()
        
        return total_chunks
    
    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """
        Add raw texts to the index.
        
        Args:
            texts: List of text chunks
            metadatas: Optional list of metadata dictionaries for each text
            
        Returns:
            List of chunk IDs
        """
        if not texts:
            return []
        
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        embeddings = self.embedder.embed_text(texts)
        
        self.index.add(embeddings)
        
        chunk_ids = []
        for i, (text, metadata) in enumerate(zip(texts, metadatas)):
            chunk_id = f"text_{int(time.time())}_{i}"
            chunk_ids.append(chunk_id)
            
            chunk_metadata = metadata.copy()
            chunk_metadata['chunk_text'] = text
            chunk_metadata['added_at'] = time.time()
            
            self.doc_ids.append(chunk_id)
            self.metadata.append(chunk_metadata)
        
        self.save_index()
        
        logger.info(f"Added {len(texts)} text chunks to index")
        return chunk_ids
    
    def search(self, query: str, top_k: int = DEFAULT_TOP_K) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query: Query string
            top_k: Number of results to return
            
        Returns:
            List of dictionaries with search results
        """
        if not self.doc_ids:
            logger.warning("Index is empty, no results to return")
            return []
        
        query_embedding = self.embedder.embed_text(query)
        
        top_k = min(top_k, len(self.doc_ids))  # Ensure we don't request more than available
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # FAISS returns -1 for padded results
                similarity = 1.0 / (1.0 + distances[0][i])
                
                chunk_metadata = self.metadata[idx].copy()
                
                result = {
                    "chunk_id": self.doc_ids[idx],
                    "text": chunk_metadata.pop('chunk_text', ''),
                    "metadata": chunk_metadata,
                    "score": float(similarity)
                }
                
                results.append(result)
        
        return results
    
    def save_index(self) -> Tuple[str, str]:
        """
        Save the index and metadata to disk.
        
        Returns:
            Tuple of (index_path, metadata_path)
        """
        faiss.write_index(self.index, str(self.index_path))
        
        metadata_obj = {
            "name": self.index_name,
            "embedding_model": self.embedder.get_model_info(),
            "doc_ids": self.doc_ids,
            "metadata": self.metadata,
            "updated_at": time.time()
        }
        
        with open(self.metadata_path, 'w') as f:
            json.dump(metadata_obj, f, indent=2)
        
        logger.info(f"Saved index with {len(self.doc_ids)} chunks to {self.index_path}")
        return str(self.index_path), str(self.metadata_path)
    
    def load_index(self) -> bool:
        """
        Load the index and metadata from disk.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.index = faiss.read_index(str(self.index_path))
            
            with open(self.metadata_path, 'r') as f:
                metadata_obj = json.load(f)
            
            self.doc_ids = metadata_obj.get('doc_ids', [])
            self.metadata = metadata_obj.get('metadata', [])
            
            logger.info(f"Loaded index with {len(self.doc_ids)} chunks from {self.index_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading index: {str(e)}")
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.doc_ids = []
            self.metadata = []
            return False
    
    def get_index_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the index.
        
        Returns:
            Dictionary with index statistics
        """
        return {
            "name": self.index_name,
            "size": len(self.doc_ids),
            "embedding_model": self.embedder.get_model_info(),
            "index_file": str(self.index_path) if self.index_path.exists() else None,
            "metadata_file": str(self.metadata_path) if self.metadata_path.exists() else None,
            "last_updated": os.path.getmtime(self.metadata_path) if self.metadata_path.exists() else None
        }
    
    def clear_index(self) -> None:
        """
        Clear the index and metadata.
        """
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.doc_ids = []
        self.metadata = []
        
        self.save_index()
        
        logger.info(f"Cleared index {self.index_name}")


def get_retriever(index_name: str = "default", embedding_model: Optional[str] = None) -> Retriever:
    """
    Factory function to get a retriever instance.
    
    Args:
        index_name: Name of the FAISS index
        embedding_model: Type of embedding model to use ('openai' or 'sentence-transformer')
        
    Returns:
        Retriever instance
    """
    return Retriever(index_name, embedding_model)


def load_documents_from_processed_dir() -> List[Dict[str, Any]]:
    """
    Load all processed documents from the processed directory.
    
    Returns:
        List of document dictionaries
    """
    documents = []
    
    for file_path in PROCESSED_DIR.glob('*.json'):
        try:
            with open(file_path, 'r') as f:
                doc = json.load(f)
                documents.append(doc)
        except Exception as e:
            logger.error(f"Failed to load document {file_path}: {str(e)}")
    
    logger.info(f"Loaded {len(documents)} documents from {PROCESSED_DIR}")
    return documents


if __name__ == "__main__":
    print("Creating retriever...")
    retriever = get_retriever("example")
    
    texts = [
        "Artificial intelligence is transforming industries across the globe.",
        "Machine learning algorithms can identify patterns in large datasets.",
        "Natural language processing enables computers to understand human language.",
        "Computer vision systems can recognize objects in images and videos."
    ]
    
    metadatas = [
        {"topic": "AI", "source": "example"},
        {"topic": "Machine Learning", "source": "example"},
        {"topic": "NLP", "source": "example"},
        {"topic": "Computer Vision", "source": "example"}
    ]
    
    print("Adding texts to index...")
    retriever.add_texts(texts, metadatas)
    
    print("\nSearching for 'AI applications'...")
    results = retriever.search("AI applications", top_k=2)
    
    for i, result in enumerate(results):
        print(f"\nResult {i+1} (Score: {result['score']:.4f}):")
        print(f"Text: {result['text']}")
        print(f"Metadata: {result['metadata']}")
    
    print("\nIndex stats:")
    stats = retriever.get_index_stats()
    for key, value in stats.items():
        print(f"- {key}: {value}")
