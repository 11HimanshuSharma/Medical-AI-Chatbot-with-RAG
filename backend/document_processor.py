import os
import PyPDF2
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

class DocumentProcessor:
    """Handles processing of medical documents"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=int(os.getenv('CHUNK_SIZE', 1000)),
            chunk_overlap=int(os.getenv('CHUNK_OVERLAP', 200)),
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def process_pdf(self, filepath: str) -> List[Document]:
        """Extract text from PDF and split into chunks"""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    text += f"\n\n--- Page {page_num + 1} ---\n\n{page_text}"
                
                # Clean the text
                text = self._clean_text(text)
                
                # Split into chunks
                chunks = self.text_splitter.split_text(text)
                
                # Create Document objects
                documents = []
                for i, chunk in enumerate(chunks):
                    doc = Document(
                        page_content=chunk,
                        metadata={
                            'source': filepath,
                            'chunk_id': i,
                            'total_chunks': len(chunks),
                            'document_type': 'medical_pdf'
                        }
                    )
                    documents.append(doc)
                
                return documents
                
        except Exception as e:
            raise Exception(f"Error processing PDF {filepath}: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        import re
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might interfere
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]]', ' ', text)
        
        # Normalize spacing around punctuation
        text = re.sub(r'\s*\.\s*', '. ', text)
        text = re.sub(r'\s*\,\s*', ', ', text)
        
        return text.strip()
    
    def extract_medical_entities(self, text: str) -> Dict:
        """Extract medical entities from text (basic implementation)"""
        # This is a simplified version - in production, you'd use medical NER models
        medical_keywords = {
            'medications': ['mg', 'ml', 'tablet', 'capsule', 'dose', 'medication', 'drug'],
            'conditions': ['diagnosis', 'syndrome', 'disease', 'disorder', 'infection'],
            'procedures': ['surgery', 'procedure', 'treatment', 'therapy', 'intervention'],
            'lab_values': ['level', 'count', 'result', 'test', 'lab', 'blood', 'urine']
        }
        
        entities = {}
        text_lower = text.lower()
        
        for category, keywords in medical_keywords.items():
            found_keywords = [kw for kw in keywords if kw in text_lower]
            if found_keywords:
                entities[category] = found_keywords
        
        return entities
