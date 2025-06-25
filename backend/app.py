import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from document_processor import DocumentProcessor
from rag_system import RAGSystem
from medical_llm import MedicalLLM

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.getenv('VECTOR_DB_PATH', './vector_db'), exist_ok=True)

# Initialize components
document_processor = DocumentProcessor()
rag_system = RAGSystem()
medical_llm = MedicalLLM()

# Store for session management
sessions = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Medical Chatbot API is running'
    })

@app.route('/api/upload', methods=['POST'])
def upload_document():
    """Upload and process medical documents"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are supported'}), 400
        
        # Save the uploaded file
        filename = str(uuid.uuid4()) + '.pdf'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the document
        text_chunks = document_processor.process_pdf(filepath)
        
        # Add to vector database
        rag_system.add_documents(text_chunks, metadata={
            'filename': file.filename,
            'filepath': filepath
        })
        
        return jsonify({
            'message': 'Document uploaded and processed successfully',
            'filename': file.filename,
            'chunks_processed': len(text_chunks)
        })
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint with RAG"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message']
        session_id = data.get('session_id', 'default')
        
        # Initialize session if needed
        if session_id not in sessions:
            sessions[session_id] = {
                'history': [],
                'context': []
            }
        
        # Retrieve relevant documents using RAG
        relevant_docs = rag_system.search_similar_documents(user_message, k=3)
        
        # Generate response using medical LLM
        response = medical_llm.generate_response(
            user_message=user_message,
            context_documents=relevant_docs,
            chat_history=sessions[session_id]['history']
        )
        
        # Update session history
        sessions[session_id]['history'].append({
            'user': user_message,
            'assistant': response
        })
        
        # Keep only last 10 exchanges to manage memory
        if len(sessions[session_id]['history']) > 10:
            sessions[session_id]['history'] = sessions[session_id]['history'][-10:]
        
        return jsonify({
            'response': response,
            'sources': [doc.metadata.get('filename', 'Unknown') for doc in relevant_docs],
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Chat failed: {str(e)}'}), 500

@app.route('/api/documents', methods=['GET'])
def list_documents():
    """List all processed documents"""
    try:
        documents = rag_system.get_document_list()
        return jsonify({'documents': documents})
    except Exception as e:
        return jsonify({'error': f'Failed to list documents: {str(e)}'}), 500

@app.route('/api/clear_session', methods=['POST'])
def clear_session():
    """Clear chat session"""
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        
        if session_id in sessions:
            sessions[session_id] = {'history': [], 'context': []}
        
        return jsonify({'message': 'Session cleared successfully'})
    except Exception as e:
        return jsonify({'error': f'Failed to clear session: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting Medical Chatbot API...")
    print("Make sure to set your OPENAI_API_KEY in the .env file")
    app.run(debug=True, host='0.0.0.0', port=5000)
