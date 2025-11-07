# YOUR NEXT THREE STEPS 🚀

**You're here:** ✅ Complete system designed and documented  
**Status:** Ready to start building!  
**Current date:** November 6, 2025

---

## 🎯 STEP 1: Set Up Your Development Environment (Today - 2-3 hours)

### What You're Doing:
Creating the project structure and installing all necessary tools

### Action Checklist:

#### 1A. Create Project Repository
```bash
# Create main project directory
mkdir human-rights-rag
cd human-rights-rag

# Initialize git
git init

# Create folder structure
mkdir -p data/{un_documents,processed,metadata}
mkdir -p src/{core,modes,intelligence,api,frontend}
mkdir -p src/api/routes
mkdir -p src/frontend/{templates,static}
mkdir -p src/frontend/static/{css,js,assets}
mkdir -p database/data
mkdir -p chromadb
mkdir -p tests
mkdir -p docs
mkdir -p scripts

# Verify structure was created
ls -R
```

#### 1B. Set Up Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Verify activation (should see (venv) in prompt)
which python
```

#### 1C. Create requirements.txt
```bash
cat > requirements.txt << 'EOF'
# Core ML/AI
sentence-transformers==2.2.2
chromadb==0.4.18
google-generativeai==0.3.1

# Web Framework
flask==3.0.0
flask-cors==4.0.0

# Data Processing
pypdf2==3.0.1
python-docx==1.1.0

# Utilities
python-dotenv==1.0.0
requests==2.31.0

# Testing
pytest==7.4.3
pytest-flask==1.3.0

# Database
sqlalchemy==2.0.23
EOF
```

#### 1D. Install Dependencies
```bash
# Install all packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E "sentence-transformers|chromadb|google-generativeai|flask"
```

#### 1E. Create Environment Variables File
```bash
cat > .env << 'EOF'
# Gemini API Key
GEMINI_API_KEY=your_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Database
DATABASE_URL=sqlite:///database/data/human_rights_rag.db

# ChromaDB
CHROMADB_PATH=./chromadb
EOF
```

**🔑 IMPORTANT:** Get your Gemini API key from: https://ai.google.dev/

#### 1F. Create .gitignore
```bash
cat > .gitignore << 'EOF'
# Python
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/

# Environment
.env
.env.local

# Databases
*.db
*.sqlite
*.sqlite3
database/data/*.db
chromadb/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
data/un_documents/*.pdf
data/processed/
logs/
EOF
```

#### 1G. Copy Planning Documents
```bash
# Copy your planning documents into the repo
cp /path/to/PROJECT_PLAN.md .
cp /path/to/SYSTEM_DESIGN_DOCUMENT.md .
cp /path/to/Human_Rights_Resources_Database.docx docs/
```

#### 1H. Initial Git Commit
```bash
git add .
git commit -m "Initial project setup with folder structure and dependencies"
```

### ✅ Success Check:
- [ ] Project folders created
- [ ] Virtual environment active
- [ ] All packages installed without errors
- [ ] .env file created with API key
- [ ] Git initialized and first commit done

**Estimated Time:** 2-3 hours  
**What You'll Have:** A clean, organized project ready for development

---

## 🎯 STEP 2: Download & Process Documents (Tomorrow - 4-6 hours)

### What You're Doing:
Gathering your knowledge base - downloading UN documents and extracting text

### Action Checklist:

#### 2A. Create Download Script
```bash
# Create the script
touch scripts/download_documents.py
```

**Edit scripts/download_documents.py:**
```python
import requests
import os
from pathlib import Path

# Document URLs from your Human_Rights_Resources_Database.docx
DOCUMENTS = {
    'foundational_rights': [
        ('udhr.pdf', 'https://www.un.org/en/udhrbook/pdf/udhr_booklet_en_web.pdf'),
        ('bill_of_rights.pdf', 'https://www.ohchr.org/sites/default/files/Documents/Publications/FactSheet2Rev.1en.pdf'),
        ('core_treaties.pdf', 'https://www.ohchr.org/sites/default/files/documents/publications/coretreatiesen.pdf'),
    ],
    'childrens_rights': [
        ('crc_official.pdf', 'https://www.ohchr.org/sites/default/files/crc.pdf'),
        ('crc_unicef.pdf', 'https://downloads.unicef.org.uk/wp-content/uploads/2010/05/UNCRC_united_nations_convention_on_the_rights_of_the_child.pdf'),
    ],
    'womens_rights': [
        ('cedaw_youth.pdf', 'https://www.unwomen.org/sites/default/files/Headquarters/Attachments/Sections/Library/Publications/2016/CEDAW-for-Youth.pdf'),
    ],
    # ... add more from your database document
}

def download_documents():
    base_path = Path('data/un_documents')
    
    for topic, docs in DOCUMENTS.items():
        topic_path = base_path / topic
        topic_path.mkdir(parents=True, exist_ok=True)
        
        for filename, url in docs:
            file_path = topic_path / filename
            
            if file_path.exists():
                print(f"✓ {filename} already exists, skipping")
                continue
            
            print(f"⬇️  Downloading {filename}...")
            try:
                response = requests.get(url, timeout=60)
                response.raise_for_status()
                
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ Downloaded {filename}")
            except Exception as e:
                print(f"❌ Error downloading {filename}: {e}")

if __name__ == '__main__':
    print("📥 Starting document download...")
    download_documents()
    print("✅ Download complete!")
```

#### 2B. Run Download Script
```bash
python scripts/download_documents.py
```

**Expected:** You'll see PDFs downloading into `data/un_documents/[topic]/`

#### 2C. Create Text Extraction Script
```bash
touch scripts/extract_text.py
```

**Edit scripts/extract_text.py:**
```python
from PyPDF2 import PdfReader
from pathlib import Path
import json

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

def process_all_documents():
    """Process all downloaded PDFs"""
    input_base = Path('data/un_documents')
    output_base = Path('data/processed')
    metadata_base = Path('data/metadata')
    
    output_base.mkdir(parents=True, exist_ok=True)
    metadata_base.mkdir(parents=True, exist_ok=True)
    
    document_count = 0
    
    for topic_dir in input_base.iterdir():
        if not topic_dir.is_dir():
            continue
        
        topic_name = topic_dir.name
        output_topic_dir = output_base / topic_name
        output_topic_dir.mkdir(exist_ok=True)
        
        print(f"\n📂 Processing {topic_name}...")
        
        for pdf_file in topic_dir.glob('*.pdf'):
            print(f"  📄 Extracting {pdf_file.name}...")
            
            text = extract_text_from_pdf(pdf_file)
            
            if text:
                # Save as text file
                txt_filename = pdf_file.stem + '.txt'
                output_file = output_topic_dir / txt_filename
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                # Create metadata
                metadata = {
                    'source_file': pdf_file.name,
                    'topic': topic_name,
                    'text_file': str(output_file),
                    'word_count': len(text.split())
                }
                
                metadata_file = metadata_base / f"{pdf_file.stem}_metadata.json"
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                print(f"  ✅ Saved {txt_filename} ({metadata['word_count']} words)")
                document_count += 1
    
    print(f"\n✅ Processed {document_count} documents!")

if __name__ == '__main__':
    print("📝 Starting text extraction...")
    process_all_documents()
    print("✅ Text extraction complete!")
```

#### 2D. Run Text Extraction
```bash
python scripts/extract_text.py
```

**Expected:** Text files appear in `data/processed/[topic]/`

#### 2E. Verify Your Data
```bash
# Check what you've got
ls -R data/processed/
ls -R data/metadata/

# Count total documents
find data/processed -name "*.txt" | wc -l

# Check a sample file
head -n 20 data/processed/foundational_rights/udhr.txt
```

### ✅ Success Check:
- [ ] 15-20 PDF documents downloaded
- [ ] Text extracted from all PDFs
- [ ] Text files organized by topic
- [ ] Metadata JSON files created
- [ ] Can read sample text files

**Estimated Time:** 4-6 hours (including download time)  
**What You'll Have:** Complete knowledge base ready for embedding

---

## 🎯 STEP 3: Build Your First RAG System (Days 3-4 - 8-10 hours)

### What You're Doing:
Creating a working RAG system that can answer questions

### Action Checklist:

#### 3A. Create Core RAG System
```bash
touch src/core/rag_system.py
```

**Edit src/core/rag_system.py:**
```python
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import google.generativeai as genai
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

class SimpleRAG:
    """Basic RAG system for human rights education"""
    
    def __init__(self, persist_directory="./chromadb"):
        print("🔧 Initializing RAG system...")
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model loaded")
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Initialize Gemini
        self.model = genai.GenerativeModel('gemini-pro')
        print("✅ Gemini model ready")
        
        # Collections for each topic
        self.collections = {}
        self.topics = [
            'foundational_rights',
            'childrens_rights',
            'womens_rights',
            'indigenous_rights',
            'minority_rights',
            'civil_political_rights',
            'freedom_expression',
            'economic_social_cultural',
            'right_to_education'
        ]
        
        print("✅ RAG system initialized")
    
    def create_collection(self, topic_name):
        """Create a ChromaDB collection for a topic"""
        try:
            collection = self.chroma_client.create_collection(
                name=topic_name,
                metadata={"description": f"Documents for {topic_name}"}
            )
            self.collections[topic_name] = collection
            print(f"✅ Created collection: {topic_name}")
            return collection
        except Exception as e:
            # Collection might already exist
            collection = self.chroma_client.get_collection(name=topic_name)
            self.collections[topic_name] = collection
            print(f"✅ Loaded existing collection: {topic_name}")
            return collection
    
    def load_documents_for_topic(self, topic_name):
        """Load documents for a specific topic"""
        print(f"📚 Loading documents for {topic_name}...")
        
        # Get or create collection
        collection = self.create_collection(topic_name)
        
        # Load text files
        topic_dir = Path(f'data/processed/{topic_name}')
        
        if not topic_dir.exists():
            print(f"⚠️  No documents found for {topic_name}")
            return
        
        doc_count = 0
        chunk_count = 0
        
        for txt_file in topic_dir.glob('*.txt'):
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple chunking by paragraphs
            chunks = [p.strip() for p in content.split('\n\n') if p.strip() and len(p.strip()) > 50]
            
            for idx, chunk in enumerate(chunks):
                # Generate embedding
                embedding = self.embedding_model.encode(chunk).tolist()
                
                # Add to collection
                collection.add(
                    documents=[chunk],
                    embeddings=[embedding],
                    ids=[f"{txt_file.stem}_chunk_{idx}"],
                    metadatas=[{
                        'source': txt_file.name,
                        'topic': topic_name,
                        'chunk_id': idx
                    }]
                )
                chunk_count += 1
            
            doc_count += 1
        
        print(f"✅ Loaded {doc_count} documents ({chunk_count} chunks) for {topic_name}")
    
    def load_all_topics(self):
        """Load documents for all topics"""
        print("📚 Loading all topics...")
        for topic in self.topics:
            self.load_documents_for_topic(topic)
        print("✅ All topics loaded!")
    
    def retrieve(self, query, topic, n_results=3):
        """Retrieve relevant documents"""
        if topic not in self.collections:
            return None
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search
        results = self.collections[topic].query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return results
    
    def generate_answer(self, query, topic, difficulty='intermediate'):
        """Complete RAG pipeline"""
        print(f"\n❓ Question: {query}")
        print(f"📂 Topic: {topic}")
        
        # Retrieve
        results = self.retrieve(query, topic)
        
        if not results or not results['documents'][0]:
            return "I couldn't find relevant information to answer that question."
        
        # Build context
        context = "\n\n".join(results['documents'][0])
        sources = [m['source'] for m in results['metadatas'][0]]
        
        # Create prompt
        prompt = f"""You are a helpful educational assistant specializing in human rights.

Context from authoritative documents:
{context}

Question: {query}

Instructions:
- Provide a clear, accurate answer based on the context
- Adjust explanation for {difficulty} level
- Be educational and helpful
- If unsure, acknowledge limitations

Answer:"""
        
        # Generate
        response = self.model.generate_content(prompt)
        answer = response.text
        
        # Add citations
        unique_sources = list(set(sources))
        citation = f"\n\n📚 Sources: {', '.join(unique_sources)}"
        
        return answer + citation

# Test function
def test_rag():
    """Test the RAG system"""
    print("=" * 60)
    print("🌍 Testing Human Rights RAG System")
    print("=" * 60)
    
    # Initialize
    rag = SimpleRAG()
    
    # Load one topic for testing
    rag.load_documents_for_topic('foundational_rights')
    
    # Test query
    query = "What are human rights?"
    answer = rag.generate_answer(query, 'foundational_rights')
    
    print("\n" + "=" * 60)
    print("ANSWER:")
    print("=" * 60)
    print(answer)
    print("=" * 60)

if __name__ == '__main__':
    test_rag()
```

#### 3B. Test Your RAG System
```bash
# Run the test
python src/core/rag_system.py
```

**Expected Output:**
- System initializes
- Loads foundational_rights documents
- Answers "What are human rights?"
- Shows source citations

#### 3C. Load All Topics
**Create scripts/initialize_system.py:**
```python
from src.core.rag_system import SimpleRAG

def initialize_all():
    print("🚀 Initializing complete RAG system...")
    rag = SimpleRAG()
    rag.load_all_topics()
    print("✅ System ready!")

if __name__ == '__main__':
    initialize_all()
```

```bash
# Run initialization
python scripts/initialize_system.py
```

**This will take 10-15 minutes** - it's creating embeddings for all documents

#### 3D. Test Multiple Topics
**Create a simple test script:**
```python
# test_queries.py
from src.core.rag_system import SimpleRAG

rag = SimpleRAG()

# Test queries for different topics
test_queries = [
    ("What is the CRC?", "childrens_rights"),
    ("What is CEDAW?", "womens_rights"),
    ("What are human rights?", "foundational_rights"),
]

for query, topic in test_queries:
    print("\n" + "="*60)
    answer = rag.generate_answer(query, topic)
    print(answer)
```

```bash
python test_queries.py
```

### ✅ Success Check:
- [ ] RAG system initializes without errors
- [ ] Can load documents for one topic
- [ ] Can answer questions with citations
- [ ] Can load all 9 topics
- [ ] Can answer questions from different topics

**Estimated Time:** 8-10 hours  
**What You'll Have:** A working RAG system that answers human rights questions!

---

## 🎉 After These 3 Steps:

**You'll have:**
1. ✅ Complete project environment set up
2. ✅ 15-20 human rights documents processed
3. ✅ Working RAG system with 9 topics
4. ✅ Ability to answer questions with citations

**You're ready for Week 2:** Building modes, quiz system, and evaluation!

---

## 📞 Need Help?

**Common Issues:**

1. **"Can't download PDFs"**
   - Check your internet connection
   - Some URLs might have changed - manually download and place in correct folder

2. **"PDF extraction fails"**
   - Some PDFs have security/encoding issues
   - Manually copy text and save as .txt file

3. **"Gemini API key error"**
   - Get key from: https://ai.google.dev/
   - Make sure it's in .env file
   - Check you've activated the API in Google Cloud Console

4. **"Out of memory"**
   - Process fewer topics at once
   - Reduce chunk size in load_documents_for_topic()

5. **"ChromaDB persistence error"**
   - Delete ./chromadb folder and try again
   - Check folder permissions

---

## 🎯 What's Next After Step 3?

Week 2 starts on Day 8 (Nov 13):
- Build Quiz Mode
- Build Lab Mode
- Add semantic routing
- Create evaluation system

**But first:** Complete these 3 steps! They're your foundation.

---

**You've got this!** 🚀

These steps are clear, achievable, and will give you a working RAG system by the end of Week 1.

**Start with Step 1 TODAY.** Set aside 2-3 hours and get your environment ready.

Good luck! 🌟
