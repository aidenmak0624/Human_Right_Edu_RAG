# 🎥 Demo & User Flow

## 🖼️ Interface Overview

The interface presents **topic cards** representing different human-rights domains. Each card leads to a conversational space powered by a Retrieval-Augmented Generation (RAG) model, making complex legal frameworks accessible through natural dialogue.

---

## ▶️ Video Walkthrough


**Video Contents:**
- Topic selection interface 
- Conversational AI interaction 
- Source citation display 

---

## 💡 User Flow

### 1. **Home Page – Topic Selection**

![Topic Selection Grid](./v1/Demo/preview.webp)

Users begin on the landing page, where they can explore **9 human rights categories**:
- 📜 Foundational Human Rights
- 👶 Children's Rights  
- 👩 Women's Rights
- 🌏 Indigenous Peoples' Rights
- 🤝 Minority Rights
- ⚖️ Civil & Political Rights
- 💬 Freedom of Expression
- 💼 Economic, Social & Cultural Rights
- 📚 Right to Education

**Design:** Responsive grid layout with icon-based navigation for intuitive topic discovery.

---

### 2. **Select a Topic**

Clicking a card transitions the interface to the **chat view**. The selected topic determines which curated knowledge base is used for retrieval.

**Example:** Selecting "Foundational Human Rights" loads documents including:
- Universal Declaration of Human Rights (UDHR)
- Bill of Rights
- Vienna Declaration
- Human Rights: A Brief Introduction

---

### 3. **Ask a Question**

![Chat Interface](./v1/Demo/preview2.jpg)

Users type any question related to the chosen topic in plain English.

**Example Questions:**
```text
What are human rights?
What is Article 29 of the UDHR?
How do civil and political rights differ from economic rights?
```

**Features:**
- Natural language processing
- Context-aware retrieval
- Loading indicator during processing
- Conversational interface (message bubbles)

---

### 4. **RAG Response**

![AI Response with Citations](./v1/Demo/preview.jpg)

The backend:
1. **Retrieves** semantically relevant document chunks from ChromaDB (0.013s)
2. **Generates** a comprehensive answer using Gemini LLM (5s)
3. **Cites** sources with relevance scores for transparency

**Response includes:**
- Detailed, educational explanation
- Multi-paragraph structure
- Key concepts highlighted
- 📚 **Sources** section with document citations and relevance scores

**Example Citation:**
```
📚 Sources: 
Human-Rights-A-brief-intro-2016.txt (score=0.846)
udhr_booklet_en_web.txt (score=0.927)
```

*Lower score = Higher relevance (distance metric)*

---

### 5. **Explore and Learn**

Users can:
- ✅ Ask follow-up questions in the same topic
- ✅ Switch to different human rights categories
- ✅ Review cited documents for deeper study
- ✅ Copy responses for notes or research

**Conversation persists** within each topic session, enabling natural dialogue flow.

---

## ⚙️ Tech Overview

### **Architecture**
```
User Query → Flask API → RAG Pipeline → ChromaDB (Retrieval)
                              ↓
                         Gemini LLM (Generation)
                              ↓
                    Answer + Source Citations
```

### **Stack Components**

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | Responsive UI, conversation interface |
| **Backend** | Flask 3.0 REST API | Request handling, CORS, routing |
| **Vector DB** | ChromaDB (persistent) | Semantic search, document embeddings |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 | Text vectorization |
| **LLM** | Google Gemini 2.5 Flash | Response generation |
| **Language** | Python 3.12 | Core application logic |

### **Performance Metrics**
- **Retrieval Speed:** 0.013s (98% faster than initial)
- **Average Response:** 5.15s (limited by LLM API)
- **Document Collections:** 9 topics, 112 chunks
- **Knowledge Base:** 25+ authoritative UN documents

---

## 📂 Quick Start

### **Prerequisites**
- Python 3.12+
- Google Gemini API key

### **Installation**

```bash
# Clone repository
git clone https://github.com/aidenmak0624/Human_Right_Edu_RAG.git
cd Human_Right_Edu_RAG

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "GOOGLE_API_KEY=your_api_key_here" > .env
echo "FLASK_SECRET_KEY=your_secret_key" >> .env
```

### **Run Application**

```bash
python -m src.api.app
```

**Access:** http://127.0.0.1:5050

**Startup time:** ~20 seconds (one-time document loading)

---

## 🎓 Educational Value

### **Why This Approach Works**

**1. Accessibility**
- Breaks down complex legal documents into conversational answers
- No prior legal knowledge required
- Natural language queries (not legal jargon)

**2. Transparency**
- Every answer includes source citations
- Relevance scores show retrieval confidence
- Users can verify information against original documents

**3. Comprehensiveness**
- Covers 9 major human rights frameworks
- 25+ authoritative sources (UN, international treaties)
- Cross-references multiple documents for complete answers

**4. Performance**
- Sub-second retrieval ensures smooth experience
- Optimized for educational use cases
- Production-ready architecture

---

## 🔗 About This Demo

This prototype demonstrates an **AI-assisted learning tool for human-rights education** — combining:
- ✅ Explainability (source citations)
- ✅ Retrieval accuracy (semantic search)
- ✅ Interactive learning (conversational AI)

**Ideal for:**
- 🎓 Educational institutions teaching international law
- 🏛️ Museums and human rights centers
- 📚 Research and reference purposes
- 💼 Engineering showcases of RAG pipelines
- 🌍 Human rights advocacy organizations

---

## 🚀 Project Highlights

### **Technical Achievements**
- **98% retrieval optimization** through document preloading
- **Production-ready performance** (5s end-to-end response)
- **Idempotent document ingestion** (content-based IDs)
- **Full-stack implementation** (frontend + backend + database)

### **Design Achievements**
- **User-centered interface** (2-click path to answers)
- **Professional UI/UX** (gradient theme, responsive grid)
- **Transparent AI** (source attribution on every response)
- **Accessible design** (icon-based navigation, clear hierarchy)

---

## 📸 Screenshots

### Landing Page
![Landing Page](./Demo/preview.webp)
*Nine human rights categories with intuitive icon-based navigation*

### Chat Interface - Loading
![Chat Loading](./Demo/preview2.jpg)
*Real-time processing indicator during RAG retrieval*

### Chat Interface - Response
![Chat Response](./Demo/preview3.jpg)
*AI-powered answers with authoritative source citations*

---

## 🔮 Future Enhancements

- [ ] **Streaming responses** for instant text display
- [ ] **Conversation history** across sessions
- [ ] **Multi-language support** (English, French, Spanish)
- [ ] **Advanced difficulty levels** (beginner/intermediate/expert)
- [ ] **Export conversations** to PDF/text
- [ ] **Mobile app** version
- [ ] **Analytics dashboard** for popular topics


**Built with:** Python • Flask • Google Gemini • ChromaDB • RAG Architecture

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Latest-orange.svg)](https://www.trychroma.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
