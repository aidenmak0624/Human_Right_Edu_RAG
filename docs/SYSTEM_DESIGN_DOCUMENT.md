# Human Rights Education RAG System - Complete Design Document

**Project:** Adaptive Educational Chatbot with Multi-Modal Learning  
**Developer:** Aiden  
**Timeline:** 3 Weeks (November 6-27, 2025)  
**Status:** Design Complete - Ready for Implementation

---

## 📋 Executive Summary

This project is an **adaptive educational chatbot system** that teaches human rights through conversational AI, leveraging RAG (Retrieval-Augmented Generation) technology with multiple learning modalities including conversational learning, quizzes, and real-world scenario analysis.

### Key Innovation Points:
- ✅ **9 specialized human rights topics** with dedicated knowledge bases
- ✅ **3 difficulty levels** with AI-powered progression tracking
- ✅ **3 learning modes**: General Chat, Quiz Mode, Lab Mode
- ✅ **Adaptive feedback system** with user-selectable styles
- ✅ **LLM-based evaluation** following educational handbook standards
- ✅ **Semantic routing** for topic relevance and intelligent redirects
- ✅ **Production-ready architecture** built on Flask + ChromaDB + Gemini API

---

## 🎯 System Overview

### Core Capabilities

**1. Multi-Topic Knowledge Base**
- 9 distinct human rights topics, each with dedicated vector databases
- Content sourced from 24+ authoritative UN and international documents
- Semantic search for accurate information retrieval

**2. Adaptive Learning System**
- User-selected difficulty levels (Beginner, Intermediate, Advanced)
- Automatic level-up recommendations after 3-4 consecutive perfect quiz scores
- LLM-based progress evaluation against educational handbook standards

**3. Multi-Modal Education**
- **General Chat Mode**: Conversational learning with AI-generated subtopics
- **Quiz Mode**: Assessment with 5 quiz options per session
- **Lab Mode**: Real-world scenario analysis with 3 scenario options

**4. Personalized Experience**
- User-selected feedback style (Positive, Corrective, Neutral)
- Semantic off-topic detection with gentle redirection
- Progress tracking across sessions

---

## 🏗️ System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────────┐  │
│  │Topic Select  │  │  Chat Interface  │  │  Feedback System     │  │
│  │(9 topics)    │→ │  + Mode Controls │  │  (Detailed Form)     │  │
│  └──────────────┘  └──────────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      FLASK REST API LAYER                           │
│                                                                     │
│  /api/chat              - Conversational Q&A                       │
│  /api/quiz/options      - Generate 5 quiz choices                  │
│  /api/quiz/start        - Begin selected quiz                      │
│  /api/quiz/submit       - Evaluate quiz answer                     │
│  /api/lab/options       - Generate 3 lab scenarios                 │
│  /api/lab/start         - Begin selected scenario                  │
│  /api/lab/submit        - Evaluate scenario analysis               │
│  /api/subtopics         - AI-generated exploration paths           │
│  /api/evaluate          - Progress evaluation                      │
│  /api/difficulty/assess - Recommend difficulty level               │
│  /api/feedback          - Collect user feedback                    │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                              │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │Mode Manager  │  │State Manager │  │  Semantic Router         │  │
│  │- General Chat│  │- Topic       │  │  - Off-topic detection   │  │
│  │- Quiz Mode   │  │- Difficulty  │  │  - Similarity threshold  │  │
│  │- Lab Mode    │  │- Progress    │  │  - Smart redirects       │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      RAG CORE SYSTEM                                │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │         9 ChromaDB Collections (Vector Databases)            │  │
│  │                                                              │  │
│  │  1. foundational_rights    6. civil_political_rights        │  │
│  │  2. childrens_rights       7. freedom_expression            │  │
│  │  3. womens_rights          8. economic_social_cultural      │  │
│  │  4. indigenous_rights      9. right_to_education            │  │
│  │  5. minority_rights                                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │         Sentence Transformers (all-MiniLM-L6-v2)             │  │
│  │         - Embedding generation                               │  │
│  │         - Semantic similarity computation                    │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                 GENERATION & EVALUATION ENGINE                      │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Gemini API                                │  │
│  │                                                              │  │
│  │  • Educational response generation                          │  │
│  │  • Quiz question creation (5 options per request)           │  │
│  │  • Lab scenario generation (3 options per request)          │  │
│  │  • AI subtopic suggestions                                  │  │
│  │  • Open-ended answer evaluation                             │  │
│  │  • Difficulty level assessment                              │  │
│  │  • Adaptive feedback (positive/corrective/neutral)          │  │
│  │  • Progress evaluation (handbook standards)                 │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                     DATA PERSISTENCE LAYER                          │
│                                                                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │Session Store     │  │Progress Tracking │  │Feedback DB      │  │
│  │- Current state   │  │- Quiz scores     │  │- User ratings   │  │
│  │- Conversation    │  │- Level progress  │  │- Comments       │  │
│  │- Mode tracking   │  │- Perfect streaks │  │- Issues         │  │
│  │(SQLite)          │  │(SQLite)          │  │(SQLite)         │  │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎨 User Interface Design

### 1. Topic Selection Screen (Entry Point)

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║           🌍 Human Rights Education Platform                   ║
║                                                                ║
║     Explore human rights through AI-powered learning          ║
║                                                                ║
║  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ ║
║  │  📜              │  │  👶              │  │  👩          │ ║
║  │  Foundational    │  │  Children's      │  │  Women's     │ ║
║  │  Human Rights    │  │  Rights          │  │  Rights      │ ║
║  │                  │  │                  │  │              │ ║
║  │  4 documents     │  │  2 documents     │  │  3 documents │ ║
║  │  Learn core      │  │  Explore the CRC │  │  Study CEDAW │ ║
║  │  principles      │  │  and protections │  │  and equality│ ║
║  └──────────────────┘  └──────────────────┘  └──────────────┘ ║
║                                                                ║
║  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ ║
║  │  🌏              │  │  🤝              │  │  ⚖️           │ ║
║  │  Indigenous      │  │  Minority        │  │  Civil &     │ ║
║  │  Rights          │  │  Rights          │  │  Political   │ ║
║  │                  │  │                  │  │              │ ║
║  │  3 documents     │  │  1 document      │  │  3 documents │ ║
║  │  UNDRIP & ILO    │  │  Anti-           │  │  ICCPR and   │ ║
║  │  169 focus       │  │  discrimination  │  │  freedoms    │ ║
║  └──────────────────┘  └──────────────────┘  └──────────────┘ ║
║                                                                ║
║  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ ║
║  │  💬              │  │  💼              │  │  📚          │ ║
║  │  Freedom of      │  │  Economic,       │  │  Right to    │ ║
║  │  Expression      │  │  Social, Cultural│  │  Education   │ ║
║  │                  │  │                  │  │              │ ║
║  │  2 documents     │  │  3 documents     │  │  2 documents │ ║
║  │  Speech & assembly│  │  ICESCR standards│  │  UNESCO guide│ ║
║  └──────────────────┘  └──────────────────┘  └──────────────┘ ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 2. Main Chat Interface (After Topic Selection)

```
╔══════════════════════════════════════════════════════════════════════╗
║  [🏠 Home]  Current: Children's Rights ▼              [💬 Feedback]  ║
╠══════════════╦═══════════════════════════════════════════════════════╣
║              ║                                                       ║
║  📊 LEVEL    ║   🤖 Welcome to Children's Rights!                    ║
║  ┌────────┐  ║      Let's explore the Convention on the Rights      ║
║  │○ Begin │  ║      of the Child together.                           ║
║  │● Inter │✓ ║                                                       ║
║  │○ Advanc│  ║   💡 AI-Generated Exploration Paths:                  ║
║  └────────┘  ║      • Introduction to the CRC                        ║
║  Progress:   ║      • Four core principles explained                 ║
║  ████░░ 60%  ║      • Rights to survival and development             ║
║  2/3 perfect ║      • Protection from violence and exploitation      ║
║              ║      • Children's participation rights                ║
║  [Suggest]   ║                                                       ║
║              ║   👤 User: What is the CRC?                           ║
║  🎯 MODE     ║                                                       ║
║  ┌────────┐  ║   🤖 Wonderful question! 🌟 The Convention on the    ║
║  │● Chat  │  ║      Rights of the Child (CRC) is an amazing         ║
║  │○ Quiz  │  ║      international treaty that protects children...   ║
║  │○ Lab   │  ║      📚 Source: CRC Official Text                     ║
║  └────────┘  ║                                                       ║
║              ║   ┌───────────────────────────────────────────────┐   ║
║  💭 FEEDBACK ║   │ What would you like to do next?               │   ║
║  ┌────────┐  ║   │ [📚 Learn More] [🔍 Explore Subtopic]        │   ║
║  │● Positv│  ║   │ [📝 Take Quiz] [🔬 Try Scenario]             │   ║
║  │○ Correc│  ║   └───────────────────────────────────────────────┘   ║
║  │○ Neutral│  ║                                                       ║
║  └────────┘  ║                                                       ║
║              ║                                                       ║
║  [ℹ️ Help]   ╠═══════════════════════════════════════════════════════╣
║              ║  💬 Your question: [____________] [Send] [🎤]         ║
╚══════════════╩═══════════════════════════════════════════════════════╝
```

### 3. Quiz Mode Interface

```
╔══════════════════════════════════════════════════════════════════════╗
║  [🏠 Home]  Current: Children's Rights ▼              [💬 Feedback]  ║
╠══════════════╦═══════════════════════════════════════════════════════╣
║              ║                                                       ║
║  [Settings]  ║   📝 Quiz Mode Activated!                             ║
║              ║                                                       ║
║  Mode: Quiz✓ ║   Select a quiz to take:                              ║
║              ║                                                       ║
║  Level:      ║   ┌─────────────────────────────────────────────┐     ║
║  Intermediate║   │ □ Quiz 1: Introduction to the CRC           │     ║
║              ║   │   • 5 questions                             │     ║
║              ║   │   • Multiple choice                         │     ║
║              ║   │   • Estimated: 5 minutes                    │     ║
║              ║   │   • Focus: Basic concepts and history       │     ║
║              ║   └─────────────────────────────────────────────┘     ║
║              ║                                                       ║
║              ║   ┌─────────────────────────────────────────────┐     ║
║              ║   │ □ Quiz 2: The Four Core Principles          │     ║
║              ║   │   • 4 questions                             │     ║
║              ║   │   • True/False + Open-ended                 │     ║
║              ║   │   • Estimated: 4 minutes                    │     ║
║              ║   │   • Focus: Non-discrimination, best interests│    ║
║              ║   └─────────────────────────────────────────────┘     ║
║              ║                                                       ║
║              ║   ┌─────────────────────────────────────────────┐     ║
║              ║   │ □ Quiz 3: CRC Articles in Practice          │     ║
║              ║   │   • 6 questions                             │     ║
║              ║   │   • Mixed format                            │     ║
║              ║   │   • Estimated: 7 minutes                    │     ║
║              ║   │   • Focus: Real-world application           │     ║
║              ║   └─────────────────────────────────────────────┘     ║
║              ║                                                       ║
║              ║   [... 2 more quizzes ...]                            ║
║              ║                                                       ║
║              ║   [🔄 Generate Different Quizzes]                     ║
║              ║                                                       ║
╚══════════════╩═══════════════════════════════════════════════════════╝
```

### 4. Lab Mode Interface

```
╔══════════════════════════════════════════════════════════════════════╗
║  [🏠 Home]  Current: Children's Rights ▼              [💬 Feedback]  ║
╠══════════════╦═══════════════════════════════════════════════════════╣
║              ║                                                       ║
║  [Settings]  ║   🔬 Lab Mode Activated!                              ║
║              ║                                                       ║
║  Mode: Lab ✓ ║   Choose a real-world scenario to analyze:            ║
║              ║                                                       ║
║  Level:      ║   ┌─────────────────────────────────────────────┐     ║
║  Intermediate║   │ □ Scenario 1: Student Climate Activism      │     ║
║              ║   │                                             │     ║
║              ║   │   "A 15-year-old wants to organize a       │     ║
║              ║   │   climate strike at school. The principal   │     ║
║              ║   │   prohibits political activities..."        │     ║
║              ║   │                                             │     ║
║              ║   │   Focus: Freedom of expression, assembly    │     ║
║              ║   │   Complexity: Moderate                      │     ║
║              ║   │   Stakeholders: Student, school, parents    │     ║
║              ║   └─────────────────────────────────────────────┘     ║
║              ║                                                       ║
║              ║   ┌─────────────────────────────────────────────┐     ║
║              ║   │ □ Scenario 2: Refugee Child Education      │     ║
║              ║   │                                             │     ║
║              ║   │   "A refugee child is denied school        │     ║
║              ║   │   enrollment due to lack of documentation..." │   ║
║              ║   │                                             │     ║
║              ║   │   Focus: Right to education, non-discrimination│  ║
║              ║   │   Complexity: Moderate                      │     ║
║              ║   │   Stakeholders: Child, school, authorities  │     ║
║              ║   └─────────────────────────────────────────────┘     ║
║              ║                                                       ║
║              ║   ┌─────────────────────────────────────────────┐     ║
║              ║   │ □ Scenario 3: Healthcare Decision Making   │     ║
║              ║   │                                             │     ║
║              ║   │   "Parents refuse medical treatment for    │     ║
║              ║   │   their child based on religious beliefs..." │    ║
║              ║   │                                             │     ║
║              ║   │   Focus: Right to health, best interests    │     ║
║              ║   │   Complexity: Complex                       │     ║
║              ║   │   Stakeholders: Child, parents, doctors, state│   ║
║              ║   └─────────────────────────────────────────────┘     ║
║              ║                                                       ║
║              ║   [🔄 Generate Different Scenarios]                   ║
║              ║                                                       ║
╚══════════════╩═══════════════════════════════════════════════════════╝
```

---

## 🧩 Key Features Specification

### 1. Topic System (9 Topics)

**Available Topics:**
1. **Foundational Human Rights** - UDHR, Bill of Rights, Vienna Declaration
2. **Children's Rights** - CRC documents
3. **Women's Rights** - CEDAW documents
4. **Indigenous Peoples' Rights** - UNDRIP, ILO 169
5. **Minority Rights** - Protection guides
6. **Civil & Political Rights** - ICCPR, freedoms
7. **Freedom of Expression & Assembly** - UNESCO standards
8. **Economic, Social & Cultural Rights** - ICESCR
9. **Right to Education** - UNESCO handbook, General Comments

**Implementation:**
- Each topic has its own ChromaDB collection
- Documents are preprocessed and chunked for optimal retrieval
- Topic switching available anytime via dropdown

---

### 2. Difficulty Level System

**Three Levels:**
- **Beginner**: Simple explanations, basic concepts, foundational knowledge
- **Intermediate**: Detailed explanations, real-world applications, analytical thinking
- **Advanced**: Complex analysis, critical evaluation, policy-level considerations

**Level-Up Mechanism:**
- User achieves 3 consecutive perfect quiz scores (100%)
- LLM evaluates readiness for next level
- System recommends level-up with user confirmation
- Progress bar shows current streak: "2/3 perfect scores"
- Non-perfect score resets the streak counter

**Difficulty Assessment:**
- Optional calibration at topic entry (2-3 questions)
- Bot suggests appropriate starting level
- User can accept or choose different level

---

### 3. Learning Modes

#### **A. General Chat Mode (Default)**

**Purpose:** Conversational learning with guided exploration

**Features:**
- Natural Q&A with educational responses
- AI-generated subtopic suggestions (5 paths)
- Context-aware action buttons after each response
- Semantic off-topic detection with gentle redirects
- Source citations for all responses

**User Controls:**
- Continue conversation freely
- Select from AI-suggested subtopics
- Switch to Quiz or Lab mode
- Change topic anytime

---

#### **B. Quiz Mode**

**Purpose:** Knowledge assessment and reinforcement

**Quiz Generation:**
- System generates **5 quiz options** per request
- Each option shows: title, description, question count, estimated time
- User selects one quiz to take
- Quiz presents questions one at a time

**Quiz Format:**
- Multiple choice
- True/False
- Open-ended (LLM-evaluated)
- Mix of formats in single quiz

**Evaluation:**
- Immediate feedback after each answer
- Positive/Corrective/Neutral style based on user preference
- Final score at quiz completion
- Progress toward level-up displayed

**Quiz Completion Flow:**
```
User selects Quiz Mode
→ Bot generates 5 quiz options
→ User picks one
→ Bot presents question 1/N
→ User answers
→ Bot evaluates and provides feedback
→ Bot presents question 2/N
→ ... continues until all questions answered
→ Bot shows final score
→ Bot checks level-up eligibility
→ [Take Another Quiz] or [Return to Chat]
```

---

#### **C. Lab Mode**

**Purpose:** Real-world scenario analysis and critical thinking

**Scenario Generation:**
- System generates **3 scenario options** per request
- Each shows: title, preview, focus rights, complexity level
- User selects one scenario to analyze

**Scenario Structure:**
- Realistic human rights situation
- Multiple stakeholders with different perspectives
- Relevant legal/policy context provided
- Open-ended analysis questions
- No single "correct" answer

**Evaluation:**
- LLM evaluates user's analysis
- Considers: rights identification, multiple perspectives, reasoning depth
- Provides constructive feedback
- Suggests areas for deeper exploration

**Lab Completion Flow:**
```
User selects Lab Mode
→ Bot generates 3 scenario options
→ User picks one
→ Bot presents full scenario + context
→ User submits analysis
→ Bot evaluates and provides detailed feedback
→ [Try Another Scenario] or [Return to Chat]
```

---

### 4. Feedback System

**Three Feedback Styles (User-Selectable):**

**Positive (Encouraging):**
- Emphasizes strengths
- Celebrates progress
- Uses motivational language
- Example: "Wonderful question! 🌟 You're on the right track..."

**Corrective (Educational):**
- Direct and constructive
- Points out misconceptions
- Provides clear explanations
- Example: "Not quite. The CRC was adopted in 1989, not 1948. Here's why..."

**Neutral (Factual):**
- Objective information only
- No emotional tone
- Straightforward presentation
- Example: "The CRC has 54 articles covering children's rights. Source: CRC Official Text"

**User selects preferred style in left sidebar, bot adjusts all responses accordingly.**

---

### 5. Semantic Routing & Off-Topic Detection

**Purpose:** Guide users to relevant content while allowing exploration

**Similarity Thresholds:**
- **> 0.6**: Clearly on-topic → Answer directly
- **0.3 - 0.6**: Related → Bridge with option to switch topics
- **< 0.3**: Off-topic → Gentle redirect to appropriate topic

**Example Flows:**

**Scenario 1: On-Topic (>0.6)**
```
Topic: Children's Rights
Query: "What is Article 13 of the CRC?"
→ Direct answer with full context
```

**Scenario 2: Related (0.3-0.6)**
```
Topic: Children's Rights
Query: "What is freedom of speech?"
→ "Freedom of speech is important! For children specifically,
   Article 13 of the CRC protects their right to express themselves...
   
   💡 Want more about freedom of speech in general?
   [Switch to 'Freedom of Expression' topic]"
```

**Scenario 3: Off-Topic (<0.3)**
```
Topic: Children's Rights
Query: "Tell me about women's rights"
→ "That's a great question! Women's rights are covered in detail
   in our 'Women's Rights' topic, which focuses on CEDAW.
   
   Would you like to:
   • Switch to Women's Rights topic?
   • Stay here and learn about girls' rights specifically?"
```

---

### 6. Progress Tracking & Evaluation

**What Gets Tracked:**
- Quiz scores and perfect score streaks
- Lab scenario completion and analysis quality
- Conversation depth and engagement
- Time spent per topic
- Current difficulty level progress

**LLM Evaluation Triggers:**
- After completing 3-5 quizzes in a topic
- When user explicitly requests progress check
- When considering level-up recommendation
- Periodically as encouragement (every 10-15 interactions)

**Evaluation Criteria (Based on Educational Handbook):**
- Factual accuracy (0-100%)
- Conceptual understanding (0-100%)
- Application ability (0-100%)
- Critical thinking depth (0-100%)

**Progress Display:**
```
📊 Your Progress in Children's Rights
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Level: Intermediate
Overall Mastery: 60%

✓ Basic concepts: Mastered
✓ Core principles: Strong understanding
⚠ Specific articles: In progress (70%)
○ Complex scenarios: Not yet started

Perfect Quiz Streak: 2/3
Next: 1 more perfect score to level up!

Recommendation: Try a Lab scenario to 
practice applying what you've learned!
```

---

### 7. AI-Generated Subtopics

**Purpose:** Guide exploration within topics

**Generation:**
- Analyzes current conversation
- Identifies what's been covered
- Suggests 5 relevant next paths
- Updates dynamically as conversation progresses

**Example:**
```
💡 AI-Generated Exploration Paths:

Current context: Just learned about CRC basics

• The four core principles of the CRC
• How the CRC is implemented in different countries
• Specific rights: Education, health, and protection
• Children's participation in decision-making
• Comparing CRC with other human rights treaties
```

---

## 💾 Data Architecture

### Database Schema (SQLite)

```sql
-- User Sessions
CREATE TABLE user_sessions (
    session_id TEXT PRIMARY KEY,
    current_topic TEXT NOT NULL,
    difficulty_level TEXT NOT NULL,
    feedback_style TEXT NOT NULL,
    current_mode TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversation History
CREATE TABLE conversation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL, -- 'user' or 'assistant'
    message TEXT NOT NULL,
    mode TEXT, -- 'chat', 'quiz', 'lab'
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id)
);

-- Quiz Tracking
CREATE TABLE quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    topic TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    quiz_title TEXT,
    questions_total INTEGER,
    questions_correct INTEGER,
    score FLOAT NOT NULL, -- 0.0 to 1.0
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id)
);

CREATE TABLE quiz_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_attempt_id INTEGER NOT NULL,
    question_number INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL, -- 'multiple_choice', 'true_false', 'open_ended'
    user_answer TEXT,
    correct_answer TEXT,
    is_correct BOOLEAN,
    feedback TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quiz_attempt_id) REFERENCES quiz_attempts(id)
);

-- Lab Scenario Tracking
CREATE TABLE lab_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    topic TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    scenario_title TEXT,
    scenario_text TEXT,
    user_analysis TEXT,
    evaluation TEXT,
    score FLOAT, -- 0.0 to 1.0
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id)
);

-- Progress Tracking
CREATE TABLE progress_evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    topic TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    factual_accuracy FLOAT,
    conceptual_understanding FLOAT,
    application_ability FLOAT,
    critical_thinking FLOAT,
    overall_mastery FLOAT,
    strengths TEXT,
    improvements TEXT,
    recommendation TEXT,
    ready_for_next_level BOOLEAN,
    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id)
);

-- Level-Up Tracking
CREATE TABLE level_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    topic TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    perfect_score_streak INTEGER DEFAULT 0,
    level_up_eligible BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id)
);

-- User Feedback
CREATE TABLE user_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    content_accuracy INTEGER, -- 1-5 stars
    explanation_clarity INTEGER, -- 1-5 stars
    overall_helpfulness INTEGER, -- 1-5 stars
    was_helpful BOOLEAN,
    comments TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id)
);
```

### Vector Database Structure (ChromaDB)

**9 Separate Collections:**
```python
collections = {
    'foundational_rights': {
        'documents': [...],
        'embeddings': [...],
        'metadatas': [
            {'source': 'udhr.pdf', 'category': 'foundational', 'article': '1'},
            ...
        ]
    },
    'childrens_rights': {...},
    'womens_rights': {...},
    'indigenous_rights': {...},
    'minority_rights': {...},
    'civil_political_rights': {...},
    'freedom_expression': {...},
    'economic_social_cultural': {...},
    'right_to_education': {...}
}
```

**Document Chunking Strategy:**
- Primary: Split by paragraphs (2-3 sentences)
- Secondary: Respect document structure (articles, sections)
- Overlap: 20-50 words between chunks
- Metadata: Source document, topic, subtopic, article number (if applicable)

---

## 🔧 Technology Stack

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **Backend Framework** | Flask | Production-ready, scalable, RESTful APIs |
| **Vector Database** | ChromaDB | Free, local, fast semantic search, easy management |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) | Free, runs locally, 384-dim vectors, good performance |
| **LLM** | Google Gemini API | Cost-effective ($0.001-0.002/query), strong reasoning |
| **Session Store** | SQLite | Simple, file-based, no setup, good for MVP |
| **Progress Database** | SQLite | Relational data, transaction support, easy queries |
| **Frontend** | Flask + HTML/CSS/JS | Clean separation, full control, production-ready |
| **Deployment** | Docker + AWS ECS | Containerized, scalable, auto-scaling capable |
| **CI/CD** | GitHub Actions | Automated testing and deployment |

---

## 📦 Project Structure

```
/human-rights-rag
│
├── /data
│   ├── /un_documents              # Raw PDF downloads (24 documents)
│   ├── /processed                 # Extracted text files by topic
│   │   ├── /foundational_rights
│   │   ├── /childrens_rights
│   │   ├── /womens_rights
│   │   └── ...
│   └── /metadata                  # Document metadata JSON files
│
├── /src
│   ├── /core                      # Core RAG system
│   │   ├── __init__.py
│   │   ├── rag_system.py          # Main RAG orchestrator
│   │   ├── embeddings.py          # Embedding generation
│   │   ├── retrieval.py           # Semantic search logic
│   │   └── collections_manager.py # Manage 9 ChromaDB collections
│   │
│   ├── /modes                     # Learning modes
│   │   ├── __init__.py
│   │   ├── mode_manager.py        # Route between modes
│   │   ├── general_chat.py        # Conversational mode
│   │   ├── quiz_mode.py           # Quiz generation & evaluation
│   │   └── lab_mode.py            # Scenario generation & evaluation
│   │
│   ├── /intelligence              # AI-powered features
│   │   ├── __init__.py
│   │   ├── llm_interface.py       # Gemini API wrapper
│   │   ├── evaluator.py           # Progress evaluation
│   │   ├── difficulty_assessor.py # Level recommendation
│   │   ├── semantic_router.py     # Off-topic detection
│   │   ├── subtopic_generator.py  # AI subtopic suggestions
│   │   └── feedback_adapter.py    # Positive/Corrective/Neutral styles
│   │
│   ├── /api                       # Flask REST API
│   │   ├── __init__.py
│   │   ├── app.py                 # Flask app initialization
│   │   ├── config.py              # Configuration management
│   │   ├── middleware.py          # Error handling, logging, CORS
│   │   ├── state_manager.py       # Session management
│   │   └── /routes
│   │       ├── __init__.py
│   │       ├── chat.py            # /api/chat endpoints
│   │       ├── quiz.py            # /api/quiz/* endpoints
│   │       ├── lab.py             # /api/lab/* endpoints
│   │       ├── subtopics.py       # /api/subtopics endpoint
│   │       ├── evaluate.py        # /api/evaluate endpoint
│   │       ├── difficulty.py      # /api/difficulty/* endpoints
│   │       └── feedback.py        # /api/feedback endpoint
│   │
│   └── /frontend                  # User interface
│       ├── /templates
│       │   ├── base.html          # Base template
│       │   ├── topic_selection.html
│       │   ├── chat_interface.html
│       │   ├── quiz_mode.html
│       │   └── lab_mode.html
│       ├── /static
│       │   ├── /css
│       │   │   └── styles.css
│       │   ├── /js
│       │   │   ├── main.js
│       │   │   ├── chat.js
│       │   │   ├── quiz.js
│       │   │   └── lab.js
│       │   └── /assets
│       │       └── icons/
│       └── streamlit_app.py       # Alternative: Streamlit version
│
├── /database
│   ├── __init__.py
│   ├── init_db.py                 # Database schema setup
│   ├── models.py                  # ORM models (if using)
│   ├── queries.py                 # Common database queries
│   └── /data                      # SQLite database files (gitignored)
│
├── /chromadb                      # Vector database storage (gitignored)
│
├── /scripts                       # Utility scripts
│   ├── download_documents.py     # Download PDFs from URLs
│   ├── extract_text.py           # PDF text extraction
│   ├── create_embeddings.py      # Generate embeddings for all documents
│   └── initialize_system.py      # Complete system initialization
│
├── /tests                         # Test suite
│   ├── __init__.py
│   ├── test_rag.py
│   ├── test_modes.py
│   ├── test_evaluation.py
│   ├── test_semantic_router.py
│   └── test_api.py
│
├── /docs                          # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── ARCHITECTURE.md
│   ├── EDUCATIONAL_DESIGN.md
│   ├── DEPLOYMENT_GUIDE.md
│   └── USER_GUIDE.md
│
├── .env                           # Environment variables (gitignored)
├── .gitignore
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container definition
├── docker-compose.yml             # Multi-container setup
├── README.md                      # Project overview
├── PROJECT_PLAN.md                # 3-week implementation plan
└── SYSTEM_DESIGN_DOCUMENT.md      # This document
```

---

## 🚀 Implementation Timeline (3 Weeks)

### **Week 1: Foundation (Nov 6-12)**

#### Days 1-2: Data Pipeline
- [x] Planning documents created
- [ ] Download 9 topics worth of documents (15-20 documents minimum)
- [ ] Extract text from PDFs
- [ ] Structure data by topic folders
- [ ] Create document metadata files

#### Days 3-4: RAG Core
- [ ] Set up 9 ChromaDB collections
- [ ] Implement embedding generation
- [ ] Implement semantic search
- [ ] Test retrieval quality with sample queries
- [ ] Optimize chunking strategy

#### Days 5-6: Flask API Basics
- [ ] Initialize Flask project structure
- [ ] Create /api/chat endpoint (basic)
- [ ] Implement session management
- [ ] Test with Postman/curl
- [ ] Add logging and error handling

#### Day 7: Basic UI
- [ ] Topic selection screen (9 cards)
- [ ] Basic chat interface layout
- [ ] Connect frontend to API
- [ ] Test end-to-end flow

**Week 1 Deliverable:** ✅ Working RAG chatbot with 9 topics, basic Q&A capability

---

### **Week 2: Intelligence & Modes (Nov 13-19)**

#### Days 8-9: Mode System
- [ ] Implement mode manager
- [ ] Create general chat mode with subtopics
- [ ] Build quiz mode with 5-option generation
- [ ] Build lab mode with 3-scenario generation
- [ ] Add mode switching logic

#### Days 10-11: AI Features
- [ ] Implement semantic router (off-topic detection)
- [ ] Build subtopic generator
- [ ] Create difficulty assessor
- [ ] Implement feedback style adapter
- [ ] Add bridge responses for related queries

#### Days 12-13: Evaluation System
- [ ] Build LLM progress evaluator
- [ ] Implement quiz scoring logic
- [ ] Create lab analysis evaluation
- [ ] Build level-up tracker (3 perfect scores)
- [ ] Add progress visualization

#### Day 14: Testing & Refinement
- [ ] Test all modes thoroughly
- [ ] Test semantic routing with edge cases
- [ ] Validate quiz and lab generation quality
- [ ] Fix bugs and improve prompts

**Week 2 Deliverable:** ✅ Full multi-mode educational system with evaluation

---

### **Week 3: Polish & Deploy (Nov 20-27)**

#### Days 15-17: UI Enhancement
- [ ] Implement left sidebar (difficulty, mode, feedback)
- [ ] Add quiz interface with 5 options display
- [ ] Add lab interface with 3 scenarios display
- [ ] Implement feedback form (top right)
- [ ] Add progress bar and streak display
- [ ] Polish CSS and responsiveness

#### Days 18-19: Database & State
- [ ] Complete SQLite schema implementation
- [ ] Implement all database queries
- [ ] Add persistent session management
- [ ] Build progress tracking dashboard
- [ ] Test data persistence

#### Days 20-21: Deployment
- [ ] Create Dockerfile
- [ ] Set up docker-compose
- [ ] Deploy to AWS ECS
- [ ] Configure environment variables
- [ ] Set up domain (optional)
- [ ] Test production deployment

#### Day 21: Documentation & Demo
- [ ] Write comprehensive README
- [ ] Complete API documentation
- [ ] Create architecture diagrams
- [ ] Record 3-5 minute demo video
- [ ] Prepare presentation slides
- [ ] Update portfolio

**Week 3 Deliverable:** ✅ Production-ready, deployed educational platform

---

## 💰 Cost Analysis

### Development Phase (3 Weeks)
**Total: $0** (All local development)
- Sentence Transformers: Free (runs locally)
- ChromaDB: Free (local storage)
- SQLite: Free
- Development environment: Free

### Deployment Phase (Monthly)
**Estimated: $20-50/month**

| Service | Cost | Notes |
|---------|------|-------|
| AWS ECS (t3.small) | $15-30/month | 2 vCPU, 2GB RAM, sufficient for demo |
| Gemini API | $5-20/month | Depends on usage; ~$0.001-0.002 per query |
| Domain name | $1/month | Optional, ~$12/year |
| **Total** | **$21-51/month** | Scales with usage |

### Cost Optimization Strategies:
- Cache common queries (reduce LLM calls)
- Use AWS free tier initially
- Implement request throttling
- Monitor and optimize expensive operations

---

## 📊 Success Metrics

### Technical Metrics
- ✅ System uptime > 99%
- ✅ Average query response time < 3 seconds
- ✅ Retrieval accuracy > 85% (correct document retrieved)
- ✅ Quiz generation quality (manual review: 9/10)
- ✅ Lab scenario relevance (manual review: 8/10)

### Educational Metrics
- ✅ User engagement time > 10 minutes per session
- ✅ Quiz completion rate > 70%
- ✅ Lab scenario completion rate > 60%
- ✅ Users reaching Intermediate level > 40%
- ✅ Users reaching Advanced level > 15%

### Portfolio Metrics
- ✅ Demonstrable to recruiters (live deployed URL)
- ✅ Comprehensive documentation
- ✅ Clean, professional codebase
- ✅ 2-3 minute demo video
- ✅ Positive feedback from 5+ testers

---

## 🎯 Competitive Advantages

### What Makes This Project Stand Out:

1. **Multi-Modal Learning** - Not just Q&A, but quizzes and real-world scenarios
2. **Adaptive Intelligence** - LLM-based evaluation following educational standards
3. **Production Architecture** - Scalable Flask API, not just a demo script
4. **Educational Rigor** - Based on actual UN documents and educational handbooks
5. **User-Centered Design** - Multiple difficulty levels, feedback styles, progress tracking
6. **Domain Expertise** - Showcases understanding of both ML/AI and human rights education
7. **Complete System** - From data ingestion to deployment, demonstrates full-stack ML skills

### Interview Talking Points:

**Technical Skills Demonstrated:**
- RAG system architecture and implementation
- Vector embeddings and semantic search
- LLM prompt engineering and evaluation
- RESTful API design
- Session and state management
- Database design and queries
- Frontend development
- Docker containerization
- Cloud deployment (AWS ECS)
- CI/CD pipeline

**ML/AI Capabilities:**
- Retrieval-Augmented Generation
- Semantic similarity computation
- Off-topic detection and classification
- Automated content generation (quizzes, scenarios)
- Progress evaluation and recommendation systems
- Adaptive learning path generation

**Soft Skills:**
- Project planning and execution
- User experience design
- Educational technology understanding
- Technical documentation
- Problem-solving and debugging

---

## 🔄 Future Enhancements (Post-MVP)

### Phase 2 Features:
- [ ] Multi-language support (French, Spanish, Mandarin, Arabic)
- [ ] User accounts and persistent profiles
- [ ] Social features (share progress, compare with peers)
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Integration with learning management systems (LMS)
- [ ] Export progress reports (PDF)
- [ ] Gamification (badges, achievements, leaderboards)

### Phase 3 Features:
- [ ] Voice interaction (speech-to-text, text-to-speech)
- [ ] Video content integration
- [ ] Collaborative learning (group scenarios)
- [ ] Teacher/administrator dashboard
- [ ] Custom content upload for educators
- [ ] Advanced difficulty calibration using item response theory
- [ ] Peer review system for open-ended answers
- [ ] Integration with official UN learning platforms

---

## 📚 Resources & References

### Technical Resources:
- ChromaDB Documentation: https://docs.trychroma.com/
- Sentence Transformers: https://www.sbert.net/
- Google Gemini API: https://ai.google.dev/docs
- Flask Documentation: https://flask.palletsprojects.com/
- AWS ECS Guide: https://docs.aws.amazon.com/ecs/

### Educational Resources:
- UN OHCHR Publications: https://www.ohchr.org/en/publications
- UNESCO Education Resources: https://www.unesco.org/en/education
- Right to Education Initiative: https://www.right-to-education.org/
- UNICEF Learning Materials: https://www.unicef.org/

### Human Rights Documents (24 sources):
- See: Human_Rights_Resources_Database.docx

---

## 👨‍💻 Developer Information

**Developer:** Aiden  
**Academic Background:** Computer Science, University of Manitoba (2025)  
**Skills Focus:** ML/AI, RAG Systems, Educational Technology  
**Languages:** English (fluent), Cantonese (fluent), Mandarin (fluent), German (beginner)

**Project Purpose:**
- Demonstrate ML/AI engineering capabilities
- Showcase end-to-end system development
- Portfolio piece for ML/AI job applications
- Contribute to human rights education accessibility

**Contact:**
- GitHub: [To be added]
- Portfolio: [To be added]
- Demo URL: [To be deployed]

---

## 📄 License & Attribution

**Project License:** [To be determined]

**Data Sources:**
- All UN documents are public domain
- OHCHR materials used for educational purposes
- Proper attribution provided in all responses

**Third-Party Libraries:**
- See requirements.txt for complete list
- All open-source libraries used in compliance with their licenses

---

## ✅ Sign-Off

This system design document represents the complete architectural plan for the Human Rights Education RAG System. All features, interfaces, and implementation details have been specified and are ready for development.

**Status:** ✅ Design Complete - Ready for Implementation  
**Next Step:** Begin Week 1 implementation following the timeline above  
**Last Updated:** November 6, 2025

---

**Document Version:** 1.0  
**Prepared By:** Claude (AI Assistant) & Aiden (Developer)  
**Date:** November 6, 2025
