
🌍 Human Rights Education Platform
An AI-powered educational platform that makes international human rights law accessible and understandable through natural language conversation. Built with Retrieval-Augmented Generation (RAG), this system provides accurate, source-backed answers to questions about human rights by drawing from 25+ authoritative documents including the Universal Declaration of Human Rights (UDHR), Convention on the Rights of the Child (CRC), and CEDAW.
The Challenge
Human rights frameworks are complex, scattered across numerous international treaties and conventions, and often difficult for students, researchers, and advocates to navigate. Traditional search methods require knowing exactly which document to consult, and legal language can be intimidating for newcomers to the field.
The Solution
This platform leverages modern AI to create an intuitive question-answering system that:

Understands natural language queries - Ask questions in plain English about any human rights topic
Provides source-backed answers - Every response includes citations to original documents with relevance scores
Covers 9 major categories - From foundational rights to specialized topics like children's rights and freedom of expression
Maintains accuracy - Uses RAG architecture to ground responses in authoritative sources, preventing AI hallucinations
Delivers fast responses - Optimized retrieval system processes queries in under 0.02 seconds

Technical Highlights
Built with production-ready performance optimization, the system achieves 98% faster retrieval through document preloading and persistent vector storage. The architecture combines Google's Gemini 2.5 Flash for generation with ChromaDB for vector search, processing 112 document chunks across a carefully curated knowledge base.
Whether you're a law student researching international standards, an educator preparing curriculum materials, or an advocate seeking quick reference to human rights principles, this platform transforms how people access and understand human rights law.
Tech Stack: Python • Flask • Google Gemini • ChromaDB • sentence-transformers • RAG Architecture

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/human_right_rag.git
cd human_right_rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
echo "FLASK_SECRET_KEY=your_secret_key_here" >> .env

# Run the application
python -m src.api.app
```

**Access the app:** http://localhost:5050

---

## 📊 Performance

| Metric | Value | Status |
|--------|-------|--------|
| Retrieval Speed | 0.013s | ✅ Excellent |
| Average Response | 5.15s | ✅ Good |
| Document Collections | 9 | 112 chunks |
| Startup Time | ~20s | One-time cost |

**Bottleneck:** Gemini API latency (3-7s) - external, expected for cloud LLMs

---

## 🏗️ System Architecture

```
User Query → Flask API → RAG System → Vector DB (ChromaDB)
                              ↓
                         Gemini LLM
                              ↓
                         Source-backed Answer
```

**Components:**
- **Frontend:** HTML/CSS/JavaScript with responsive grid
- **Backend:** Flask REST API with CORS
- **LLM:** Google Gemini 2.5 Flash
- **Embeddings:** sentence-transformers/all-MiniLM-L6-v2
- **Vector DB:** ChromaDB (persistent)

---

## 📡 API Endpoints

### POST `/api/chat`
Process a human rights question with RAG.

**Request:**
```json
{
  "query": "What are human rights?",
  "topic": "foundational_rights",
  "difficulty": "intermediate"
}
```

**Response:**
```json
{
  "answer": "Human rights are...",
  "sources": ["udhr.txt (score=0.234)", "..."],
  "topic": "foundational_rights",
  "query": "What are human rights?"
}
```

### GET `/api/topics`
List all available topic categories.

### GET `/api/health`
Health check endpoint.

---

## 📚 Available Topics

| Icon | Topic | Description |
|------|-------|-------------|
| 📜 | Foundational Human Rights | UDHR, Bill of Rights, Vienna Declaration |
| 👶 | Children's Rights | Convention on the Rights of the Child |
| 👩 | Women's Rights | CEDAW and gender equality |
| 🌏 | Indigenous Peoples' Rights | UNDRIP and ILO 169 |
| 🤝 | Minority Rights | Protection and anti-discrimination |
| ⚖️ | Civil & Political Rights | ICCPR and fundamental freedoms |
| 💬 | Freedom of Expression | Speech and assembly rights |
| 💼 | Economic, Social & Cultural Rights | ICESCR standards |
| 📚 | Right to Education | Educational rights and access |

---

## 🔧 Recent Updates (Nov 7, 2025)

### Performance Optimization
- ✅ Implemented document preloading (98% faster retrieval)
- ✅ Optimized ChromaDB persistence
- ✅ Reduced average response time by 25%

### Bug Fixes
- ✅ Resolved Flask blueprint naming conflict
- ✅ Fixed API route path configuration
- ✅ Improved error handling

See [PROGRESS_LOG_2025-11-07.md](./PROGRESS_LOG_2025-11-07.md) for detailed changelog.

---

## 🔮 Roadmap

- [ ] Implement streaming responses (SSE)
- [ ] Build interactive chat interface
- [ ] Add conversation history
- [ ] Response caching for common queries
- [ ] Multi-language support
- [ ] Docker containerization
- [ ] CI/CD pipeline




