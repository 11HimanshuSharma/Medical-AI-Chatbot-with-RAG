<!-- @format -->

# Medical AI Chatbot with RAG

A sophisticated AI-powered chatbot designed to assist healthcare professionals
(doctors, nurses) and patients by providing accurate, source-backed answers from
medical documents using Retrieval-Augmented Generation (RAG).

![Medical Chatbot](https://img.shields.io/badge/Medical-AI%20Chatbot-blue)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?logo=flask)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?logo=typescript)

## 🤔 What is this?

**Simply put**: This is an intelligent medical assistant that can answer your medical questions by searching through uploaded medical documents and providing evidence-based responses.

**Think of it like**: Having a medical librarian that can instantly search through thousands of medical papers, guidelines, and documents to find relevant information and explain it to you in a conversational way.

### Why is this special?

Unlike general AI chatbots that might give generic answers, this system:
- ✅ **Only uses information from YOUR uploaded medical documents**
- ✅ **Shows you exactly which document and page the answer came from**
- ✅ **Understands medical terminology and context**
- ✅ **Provides safety disclaimers for medical advice**
- ✅ **Never makes up information** - if it doesn't know, it says so

## 🏥 Overview

This medical chatbot leverages cutting-edge AI technology to provide reliable
medical information by searching through uploaded medical documents and
generating contextually accurate responses. The system uses RAG
(Retrieval-Augmented Generation) to ensure all answers are grounded in verified
medical literature.

### What is RAG (Retrieval-Augmented Generation)?

RAG is a technique that combines two powerful AI capabilities:

1. **Retrieval**: Searching through your documents to find relevant information
2. **Generation**: Using AI to create human-like responses based on that information

**How it works in simple terms**:
```
Your Question → Search Documents → Find Relevant Info → Generate Answer + Sources
```

This means the AI doesn't just "make up" answers - it always references specific documents you've uploaded.

### Key Features

- 🔍 **Document-Based Responses**: Answers backed by uploaded medical documents
- 📄 **PDF Document Processing**: Upload and process medical PDFs, research
  papers, guidelines
- 🧠 **RAG Implementation**: Advanced retrieval system with vector embeddings
- 💊 **Medical Specialization**: Optimized for medical terminology and contexts
- 🔒 **Source Attribution**: All responses include source references
- 💬 **Real-time Chat**: Interactive chat interface with typing indicators
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │────│  Flask Backend  │────│  Vector Database│
│                 │    │                 │    │                 │
│ • Chat Interface│    │ • RAG System    │    │ • FAISS/Chroma  │
│ • File Upload   │    │ • LLM Integration│   │ • Embeddings    │
│ • Document Mgmt │    │ • Doc Processing│    │ • Similarity    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔄 How Does It Work?

### Step-by-Step Workflow

#### 1. **Document Upload & Processing**
```
📄 PDF Upload → 📝 Text Extraction → ✂️ Text Chunking → 🧮 Create Embeddings → 💾 Store in Database
```
- You upload medical PDFs (research papers, guidelines, drug sheets, etc.)
- The system extracts text and breaks it into meaningful chunks
- Each chunk gets converted into a "vector embedding" (numerical representation)
- All embeddings are stored in a searchable database

#### 2. **Question Processing & Search**
```
❓ Your Question → 🧮 Convert to Embedding → 🔍 Search Similar Chunks → 📋 Retrieve Top Matches
```
- When you ask a question, it's converted into the same type of vector embedding
- The system searches for document chunks with similar embeddings
- Top 3-5 most relevant chunks are retrieved as context

#### 3. **AI Response Generation**
```
📋 Context + ❓ Question → 🤖 AI Processing → 💬 Response + 📚 Sources
```
- The AI model (GPT) receives your question plus the relevant document chunks
- It generates a response based ONLY on the provided context
- The response includes citations showing which documents were used

### Example Workflow

**You upload**: `diabetes_guidelines.pdf`, `metformin_info.pdf`

**You ask**: *"What's the starting dose for metformin in type 2 diabetes?"*

**System process**:
1. 🔍 Searches embeddings for content related to "metformin", "dose", "type 2 diabetes"
2. 📄 Finds relevant chunks from both PDFs
3. 🤖 AI generates response: *"According to the diabetes guidelines (page 23), the recommended starting dose for metformin in type 2 diabetes is 500mg twice daily..."*
4. 📚 Shows sources: `diabetes_guidelines.pdf` and `metformin_info.pdf`

### What Makes This Reliable?

- **No hallucination**: AI can only use information from your documents
- **Source tracking**: Every answer shows exactly where the information came from
- **Medical context**: Specialized prompting for medical accuracy
- **Safety first**: Always includes disclaimers about consulting healthcare providers

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v16 or higher)
- **Python** (3.8 or higher)
- **npm** or **yarn**
- **Git**

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/medical-ai-chatbot.git
   cd medical-ai-chatbot
   ```

2. **Install Frontend Dependencies**

   ```bash
   cd frontend
   npm install
   ```

3. **Install Backend Dependencies**

   ```bash
   cd ../backend
   pip install -r requirements.txt
   ```

4. **Environment Setup**

   ```bash
   # Create .env file in backend directory
   cp .env.example .env

   # Add your API keys
   OPENAI_API_KEY=your_openai_api_key_here
   HUGGINGFACE_API_KEY=your_huggingface_key_here  # Optional
   ```

### Running the Application

1. **Start the Backend Server**

   ```bash
   cd backend
   python app.py
   ```

   Server runs on `http://localhost:5000`

2. **Start the Frontend Development Server**
   ```bash
   cd frontend
   npm run dev
   ```
   Application runs on `http://localhost:5173`

## 📋 Project Structure

```
medical-ai-chatbot/
├── 📁 frontend/                 # React TypeScript frontend
│   ├── 📁 src/
│   │   ├── 📁 components/       # React components
│   │   │   ├── ChatInput.jsx    # Chat input component
│   │   │   ├── ChatMessage.jsx  # Message display component
│   │   │   ├── DocumentUpload.jsx # Document upload interface
│   │   │   ├── EmptyState.jsx   # Empty chat state
│   │   │   ├── Header.jsx       # Application header
│   │   │   └── TypingIndicator.jsx # Typing animation
│   │   ├── App.tsx              # Main application component
│   │   ├── main.tsx             # Application entry point
│   │   └── index.css            # Global styles
│   ├── package.json             # Frontend dependencies
│   ├── vite.config.ts           # Vite configuration
│   └── tailwind.config.js       # Tailwind CSS configuration
├── 📁 backend/                  # Python Flask backend
│   ├── app.py                   # Main Flask application
│   ├── medical_llm.py           # LLM integration
│   ├── rag_system.py            # RAG implementation
│   ├── document_processor.py    # Document processing utilities
│   └── requirements.txt         # Python dependencies
├── 📁 uploads/                  # Uploaded documents storage
├── 📁 vector_db/               # Vector database storage
└── README.md                   # Project documentation
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# LLM Configuration
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_key_here

# Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB

# Vector Database
VECTOR_DB_PATH=vector_db
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### Supported Document Types

- **PDF**: Medical research papers, treatment guidelines
- **TXT**: Plain text medical documents
- **DOCX**: Word documents (coming soon)
- **JSON**: Structured medical data (coming soon)

## 💡 Usage

### 1. Upload Medical Documents

1. **Click** on "Upload Medical Documents" button
2. **Select** PDF files containing medical information:
   - 📋 Clinical practice guidelines
   - 🔬 Research papers and studies
   - 💊 Drug information sheets
   - 🏥 Treatment protocols
   - 📊 Lab reference ranges
   - 🩺 Diagnostic criteria
3. **Wait** for processing completion (usually 10-30 seconds per document)
4. **Verify** documents are indexed and ready for querying

### 2. Ask Medical Questions

#### Basic Questions
```
• "What are the side effects of metformin?"
• "What is the recommended dosage for hypertension treatment?"
• "Show me drug interactions for warfarin"
• "What are the latest guidelines for diabetes management?"
```

#### Advanced Queries
```
• "Compare the efficacy of ACE inhibitors vs ARBs for heart failure"
• "What are the contraindications for beta-blockers in COPD patients?"
• "Explain the mechanism of action of SGLT2 inhibitors"
• "What are the diagnostic criteria for metabolic syndrome?"
```

#### Clinical Scenarios
```
• "A 65-year-old patient with diabetes and CKD - what glucose targets should I aim for?"
• "How do I adjust warfarin dosing based on INR results?"
• "What antibiotics are first-line for community-acquired pneumonia?"
```

### 3. Review Source References

Each response includes:

- **📄 Source document** name (e.g., "ADA_Diabetes_Guidelines_2024.pdf")
- **📍 Page number** or section reference
- **🎯 Confidence score** (how relevant the source is)
- **📝 Relevant excerpt** from the original document
- **⚠️ Medical disclaimers** appropriate for the content

## ❓ Frequently Asked Questions (FAQ)

### **Q: How accurate are the responses?**
**A:** The system only uses information from YOUR uploaded documents, so accuracy depends on the quality of your source materials. It never "makes up" information and always cites sources.

### **Q: Can I use this for patient care decisions?**
**A:** ⚠️ **NO** - This is for educational and reference purposes only. Always consult current clinical guidelines and healthcare professionals for patient care decisions.

### **Q: What types of documents work best?**
**A:** High-quality medical PDFs with clear text work best:
- ✅ Official clinical guidelines
- ✅ Peer-reviewed research papers
- ✅ Drug monographs
- ✅ Clinical protocols
- ❌ Scanned documents with poor OCR
- ❌ Image-heavy documents

### **Q: How do I know if the AI found relevant information?**
**A:** The system shows:
- Confidence scores for each source
- Exact text excerpts from documents
- Clear citations with page numbers
- If no relevant information is found, it will say so

### **Q: Can multiple people use this simultaneously?**
**A:** Yes, the system supports multiple chat sessions. Each user gets their own conversation history while sharing the same document database.

### **Q: How long does document processing take?**
**A:** 
- Small PDFs (< 50 pages): 10-30 seconds
- Large PDFs (100+ pages): 1-3 minutes
- Very large documents: Up to 5 minutes

### **Q: What happens if I ask about something not in my documents?**
**A:** The AI will clearly state that it doesn't have relevant information in the uploaded documents and recommend uploading additional sources or consulting other references.

## 👥 Who Should Use This?

### **🩺 Healthcare Professionals**
- **Doctors**: Quick reference for treatment protocols and drug information
- **Nurses**: Access to care guidelines and medication details
- **Pharmacists**: Drug interaction checks and dosing information
- **Medical Students**: Study aid with source-backed answers
- **Researchers**: Synthesize information from multiple papers

### **🏥 Medical Organizations**
- **Hospitals**: Internal guideline distribution and reference
- **Clinics**: Standardized protocol access
- **Medical Schools**: Educational resource with citation tracking
- **Research Institutions**: Literature review assistance

### **⚠️ Not Suitable For**
- **Direct patient care** without professional oversight
- **Emergency medical decisions**
- **Replacing clinical judgment**
- **Legal medical advice**

## 🛠️ Troubleshooting

### **Document Upload Issues**
```
Problem: "Upload failed" or "Processing error"
Solutions:
✅ Ensure PDF is not password-protected
✅ Check file size < 16MB
✅ Verify PDF contains selectable text (not scanned images)
✅ Try uploading one document at a time
```

### **Poor Response Quality**
```
Problem: AI gives irrelevant or "I don't know" responses
Solutions:
✅ Upload more relevant documents
✅ Be more specific in your questions
✅ Check if documents actually contain the information
✅ Try rephrasing your question
```

### **Slow Performance**
```
Problem: Long response times
Solutions:
✅ Upload smaller documents (split large PDFs)
✅ Reduce number of uploaded documents
✅ Check your internet connection
✅ Try during off-peak hours
```

### **Technical Issues**
```
Problem: Cannot connect to backend
Solutions:
✅ Ensure backend server is running (port 5000)
✅ Check if frontend is pointing to correct API URL
✅ Verify environment variables are set
✅ Check console for error messages
```

## 🧪 API Documentation

### Chat Endpoint

**POST** `/api/chat`

```json
{
  "message": "What are the side effects of aspirin?",
  "conversation_id": "optional-conversation-id"
}
```

**Response:**

```json
{
  "response": "According to the uploaded medical guidelines...",
  "sources": [
    {
      "document": "drug_guidelines.pdf",
      "page": 15,
      "confidence": 0.89,
      "excerpt": "Aspirin may cause..."
    }
  ],
  "conversation_id": "uuid-string"
}
```

### Document Upload Endpoint

**POST** `/api/upload`

```bash
curl -X POST -F "file=@medical_document.pdf" http://localhost:5000/api/upload
```

## 🧠 Technical Details

### RAG Implementation

1. **Document Ingestion**: PDF parsing with PyPDF2/pdfplumber
2. **Text Chunking**: Semantic chunking with overlap
3. **Embedding Generation**: Sentence transformers for vector representations
4. **Vector Storage**: FAISS for efficient similarity search
5. **Retrieval**: Top-k similarity search with relevance scoring
6. **Generation**: LLM synthesis with retrieved context

### LLM Integration

- **Primary**: OpenAI GPT-3.5/4 for high-quality responses
- **Fallback**: Hugging Face Transformers for offline capability
- **Prompt Engineering**: Medical-specific prompts for accuracy

### Security Considerations

- File upload validation and sanitization
- Rate limiting on API endpoints
- Input sanitization for LLM queries
- No storage of sensitive patient data

## 🚀 Deployment


### Production Deployment

1. **Frontend Build**

   ```bash
   cd frontend
   npm run build
   ```

2. **Backend Production Server**
   ```bash
   cd backend
   gunicorn --bind 0.0.0.0:5000 app:app
   ```

### Development Guidelines

- Follow TypeScript/JavaScript best practices
- Write comprehensive tests
- Update documentation for new features
- Follow medical data handling guidelines
- Ensure HIPAA compliance considerations

## ✅ Benefits & Limitations

### **🎯 Key Benefits**

✅ **Evidence-Based Responses**: Every answer is grounded in your uploaded documents
✅ **Source Transparency**: Always shows exactly where information comes from
✅ **Medical Context**: Understands medical terminology and relationships
✅ **Safety First**: Built-in medical disclaimers and safety considerations
✅ **No Hallucination**: Cannot make up information - only uses provided sources
✅ **Instant Access**: Search through thousands of pages in seconds
✅ **Conversation Memory**: Maintains context across multiple questions
✅ **Multiple Formats**: Handles various PDF types and document structures

### **⚠️ Important Limitations**

❌ **Not for Emergency Care**: Cannot handle urgent medical situations
❌ **Document Dependent**: Quality limited by uploaded document quality
❌ **No Real-Time Updates**: Doesn't access latest medical literature automatically
❌ **Text-Only**: Cannot interpret medical images, charts, or complex diagrams
❌ **No Patient Data**: Cannot access patient records or lab results
❌ **General AI Limitations**: May occasionally misinterpret context
❌ **Requires Technical Setup**: Not plug-and-play for non-technical users

### **🎯 Best Use Cases**

🟢 **Excellent for:**
- Quick reference during study or research
- Checking drug interactions and dosages
- Finding specific guidelines or protocols
- Literature review assistance
- Educational Q&A with citations

🟡 **Okay for:**
- General medical knowledge questions
- Comparing treatment options
- Understanding medical concepts

🔴 **Not for:**
- Diagnosing patients
- Emergency medical decisions
- Legal medical advice
- Replacing clinical judgment

## ⚠️ Disclaimer

**Important**: This chatbot is for educational and informational purposes only.
It should not be used as a substitute for professional medical advice,
diagnosis, or treatment. Always consult with qualified healthcare professionals
for medical decisions.



## 🏆 Acknowledgments

- **Hugging Face** for transformer models and embeddings
- **OpenAI** for GPT models
- **LangChain** for RAG framework inspiration
- **Medical Community** for guidance on healthcare AI best practices


