import os
import chromadb
from typing import List, Dict, Any
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import uuid

class RAGSystem:
    """Retrieval-Augmented Generation system for medical documents"""
    
    def __init__(self):
        self.embedding_model_name = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
        self.vector_db_path = os.getenv('VECTOR_DB_PATH', './vector_db')
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model_name,
            model_kwargs={'device': 'cpu'}  # Use 'cuda' if you have GPU
        )
        
        # Initialize vector store
        self.vector_store = Chroma(
            persist_directory=self.vector_db_path,
            embedding_function=self.embeddings,
            collection_name="medical_documents"
        )
        
        print(f"RAG System initialized with {self.get_document_count()} documents")
    
    def add_documents(self, documents: List[Document], metadata: Dict = None):
        """Add documents to the vector database"""
        try:
            # Add additional metadata if provided
            if metadata:
                for doc in documents:
                    doc.metadata.update(metadata)
            
            # Generate unique IDs for documents
            ids = [str(uuid.uuid4()) for _ in documents]
            
            # Add to vector store
            self.vector_store.add_documents(documents, ids=ids)
            
            # Persist the changes
            self.vector_store.persist()
            
            print(f"Added {len(documents)} document chunks to vector database")
            
        except Exception as e:
            raise Exception(f"Error adding documents to vector store: {str(e)}")
    
    def search_similar_documents(self, query: str, k: int = 3, score_threshold: float = 0.7) -> List[Document]:
        """Search for similar documents using semantic similarity"""
        try:
            # Enhance query for medical context
            enhanced_query = self._enhance_medical_query(query)
            
            # Perform similarity search
            results = self.vector_store.similarity_search_with_score(
                enhanced_query, 
                k=k
            )
            
            # Filter by score threshold and return documents
            filtered_results = [
                doc for doc, score in results 
                if score >= score_threshold
            ]
            
            return filtered_results[:k]
            
        except Exception as e:
            print(f"Error in similarity search: {str(e)}")
            return []
    
    def _enhance_medical_query(self, query: str) -> str:
        """Enhance query with medical context for better retrieval"""
        medical_context_words = [
            "medical", "clinical", "treatment", "diagnosis", "patient", 
            "symptom", "condition", "therapy", "medication", "dosage"
        ]
        
        # Add medical context if not present
        query_lower = query.lower()
        has_medical_context = any(word in query_lower for word in medical_context_words)
        
        if not has_medical_context:
            query = f"medical clinical {query}"
        
        return query
    
    def get_document_count(self) -> int:
        """Get the total number of documents in the vector store"""
        try:
            # This is a workaround as Chroma doesn't have a direct count method
            collection = self.vector_store._collection
            return collection.count()
        except:
            return 0
    
    def get_document_list(self) -> List[Dict]:
        """Get list of all documents with metadata"""
        try:
            collection = self.vector_store._collection
            results = collection.get()
            
            # Group by source file
            documents = {}
            for i, metadata in enumerate(results['metadatas']):
                filename = metadata.get('filename', 'Unknown')
                if filename not in documents:
                    documents[filename] = {
                        'filename': filename,
                        'chunks': 0,
                        'document_type': metadata.get('document_type', 'unknown')
                    }
                documents[filename]['chunks'] += 1
            
            return list(documents.values())
            
        except Exception as e:
            print(f"Error getting document list: {str(e)}")
            return []
    
    def delete_document(self, filename: str):
        """Delete all chunks of a specific document"""
        try:
            collection = self.vector_store._collection
            results = collection.get()
            
            # Find IDs of chunks belonging to this document
            ids_to_delete = []
            for i, metadata in enumerate(results['metadatas']):
                if metadata.get('filename') == filename:
                    ids_to_delete.append(results['ids'][i])
            
            # Delete the chunks
            if ids_to_delete:
                collection.delete(ids=ids_to_delete)
                self.vector_store.persist()
                print(f"Deleted {len(ids_to_delete)} chunks for document: {filename}")
                
        except Exception as e:
            raise Exception(f"Error deleting document: {str(e)}")
    
    def clear_all_documents(self):
        """Clear all documents from the vector store"""
        try:
            collection = self.vector_store._collection
            collection.delete()
            self.vector_store.persist()
            print("All documents cleared from vector database")
            
        except Exception as e:
            raise Exception(f"Error clearing documents: {str(e)}")
