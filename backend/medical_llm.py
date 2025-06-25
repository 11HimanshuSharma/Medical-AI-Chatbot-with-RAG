import os
from typing import List, Dict, Any
from langchain.schema import Document
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

class MedicalLLM:
    """Medical-focused Language Model for generating responses"""
    
    def __init__(self):
        self.model_name = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
        
        # Check if OpenAI API key is available
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            print("Warning: OPENAI_API_KEY not found. Using fallback responses.")
            self.llm = None
        else:
            self.llm = ChatOpenAI(
                model_name=self.model_name,
                temperature=0.1,  # Low temperature for consistent medical responses
                max_tokens=500,
                openai_api_key=self.openai_api_key
            )
        
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Create a comprehensive system prompt for medical assistance"""
        return """You are MedBot AI, a knowledgeable medical assistant designed to help healthcare professionals and patients with medical information. Your responses should be:

GUIDELINES:
1. Accurate and evidence-based, drawing from provided medical documents
2. Clear and accessible to both medical professionals and patients
3. Always include appropriate disclaimers about seeking professional medical advice
4. Cite sources when available from the provided documents
5. If unsure, clearly state limitations and recommend professional consultation

RESPONSE STRUCTURE:
- Provide direct, helpful answers based on the context
- Include relevant medical details when appropriate
- Add safety disclaimers for patient-facing responses
- Suggest when to seek immediate medical attention if relevant

SAFETY:
- Never provide emergency medical advice
- Always recommend consulting healthcare providers for diagnosis
- Be clear about what information comes from documents vs. general knowledge
- Emphasize that AI cannot replace professional medical judgment

CONTEXT: You have access to medical documents including treatment guidelines, drug interaction information, lab result documentation, and medical research papers."""
    
    def generate_response(self, user_message: str, context_documents: List[Document], chat_history: List[Dict] = None) -> str:
        """Generate a medical response using RAG context"""
        
        # If no LLM available, use fallback
        if not self.llm:
            return self._generate_fallback_response(user_message, context_documents)
        
        try:
            # Prepare context from documents
            context = self._prepare_context(context_documents)
            
            # Prepare chat history
            history_text = self._prepare_history(chat_history or [])
            
            # Create the prompt
            prompt = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(self.system_prompt),
                HumanMessagePromptTemplate.from_template("""
Context from Medical Documents:
{context}

Previous Conversation:
{history}

Current Question: {question}

Please provide a helpful, accurate response based on the medical context provided. If the documents don't contain relevant information, clearly state this and provide general medical guidance while emphasizing the need for professional consultation.
""")
            ])
            
            # Generate response
            messages = prompt.format_messages(
                context=context,
                history=history_text,
                question=user_message
            )
            
            response = self.llm(messages)
            return response.content
            
        except Exception as e:
            print(f"Error generating LLM response: {str(e)}")
            return self._generate_fallback_response(user_message, context_documents)
    
    def _prepare_context(self, documents: List[Document]) -> str:
        """Prepare context from retrieved documents"""
        if not documents:
            return "No relevant medical documents found for this query."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            filename = doc.metadata.get('filename', 'Unknown document')
            chunk_id = doc.metadata.get('chunk_id', '')
            
            context_parts.append(f"""
Document {i}: {filename} (Section {chunk_id})
Content: {doc.page_content[:800]}...
""")
        
        return "\n".join(context_parts)
    
    def _prepare_history(self, chat_history: List[Dict]) -> str:
        """Prepare chat history for context"""
        if not chat_history:
            return "No previous conversation."
        
        history_parts = []
        for exchange in chat_history[-3:]:  # Last 3 exchanges
            history_parts.append(f"User: {exchange.get('user', '')}")
            history_parts.append(f"Assistant: {exchange.get('assistant', '')}")
        
        return "\n".join(history_parts)
    
    def _generate_fallback_response(self, user_message: str, context_documents: List[Document]) -> str:
        """Generate fallback response when LLM is not available"""
        
        # Check if we have relevant documents
        if context_documents:
            doc_info = []
            for doc in context_documents[:2]:
                filename = doc.metadata.get('filename', 'Medical document')
                content_preview = doc.page_content[:200] + "..."
                doc_info.append(f"From {filename}: {content_preview}")
            
            document_context = "\n\n".join(doc_info)
            
            return f"""Based on the medical documents in our database, here's relevant information for your query:

{document_context}

⚠️ **Important Medical Disclaimer**: 
This information is retrieved from uploaded medical documents and is for educational purposes only. It should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions.

🔍 **Recommendation**: For personalized medical advice regarding "{user_message}", please consult with your healthcare provider who can evaluate your specific situation.

💡 **Note**: This response is generated using document retrieval. For more detailed analysis, please ensure relevant medical documents are uploaded to the system."""

        else:
            return f"""I understand you're asking about: "{user_message}"

Currently, I don't have specific medical documents uploaded that directly address your question. To provide you with evidence-based information, please:

1. **Upload relevant medical documents** such as:
   - Treatment guidelines
   - Research papers
   - Clinical protocols
   - Drug information sheets

2. **Consult healthcare professionals** for personalized medical advice

⚠️ **Important**: This AI system requires uploaded medical documents to provide specific information. For immediate medical concerns, please contact your healthcare provider or emergency services.

🔧 **System Status**: Currently operating in document-retrieval mode. Upload medical PDFs to enable comprehensive responses."""
    
    def classify_medical_urgency(self, message: str) -> str:
        """Classify the urgency level of a medical query"""
        urgent_keywords = [
            'emergency', 'urgent', 'severe pain', 'chest pain', 'difficulty breathing',
            'unconscious', 'bleeding', 'stroke', 'heart attack', 'overdose', 'poisoning'
        ]
        
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in urgent_keywords):
            return "urgent"
        elif any(word in message_lower for word in ['pain', 'symptoms', 'side effects']):
            return "moderate"
        else:
            return "routine"
