# 🤖 MindMigo AI Study Buddy

**Transform Learning Into an Engaging Adventure with AI-Powered Personalization**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.118+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 One-Sentence Pitch

MindMigo is an intelligent AI study companion that gamifies learning by generating adaptive quizzes, visualizing knowledge graphs, providing personalized tutoring, and tracking progress to make education fun, engaging, and tailored to each student's unique learning journey.

---

## ✨ Key Features

### 🎮 **Gamification System**
- **XP & Leveling**: Earn experience points for completing quizzes, creating knowledge graphs, and daily challenges
- **Badge Collection**: Unlock 14+ unique badges for achievements like "Quiz Master," "Streak Champion," and "Knowledge Explorer"
- **Daily Streaks**: Maintain learning consistency with streak tracking and rewards
- **Leaderboards**: Compete with peers and climb the global rankings
- **Real-time Progress**: Visual progress bars showing XP, level advancement, and achievements

### 📝 **Adaptive Quiz Generator**
- **Dynamic Question Generation**: AI creates unique questions tailored to any topic using Groq's LLaMA 3.1 model
- **Multiple Question Types**: Support for Multiple Choice Questions (MCQs) and Fill-in-the-Blank formats
- **Difficulty Levels**: Choose from Easy, Medium, or Hard difficulty to match your skill level
- **Smart Duplicate Prevention**: Advanced algorithms ensure question uniqueness and variety
- **Instant Feedback**: Get immediate answers and explanations after quiz completion
- **Progress Tracking**: Records every attempt with accuracy metrics and topic performance

### 🕸️ **Interactive Knowledge Graph Visualization**
- **Visual Learning**: Transform complex topics into interactive node-based knowledge graphs
- **Dual Input Modes**: Generate graphs from topics or custom text content
- **Fullscreen Viewing**: Expand graphs for detailed exploration
- **Relationship Mapping**: Understand connections between concepts visually
- **PyVis Integration**: Beautiful, physics-based graph rendering

### 💬 **AI Tutor Chat**
- **24/7 Intelligent Assistant**: Get instant help on any topic, anytime
- **Context-Aware Responses**: AI remembers conversation history for coherent discussions
- **Socratic Method**: Guides students to discover answers through thoughtful questioning
- **Multi-Topic Support**: Covers unlimited subjects from math to history to programming
- **Conversation Persistence**: Chat history saved in database for continuity

### 🎯 **Daily Challenge System**
- **Fresh Problems Daily**: New challenging problem every 24 hours
- **Difficulty Variety**: Problems range from beginner to advanced
- **Streak Building**: Maintain daily solving streaks for bonus XP
- **Performance Stats**: Track solved count, accuracy rate, and streak milestones

### 📊 **Comprehensive Progress Dashboard**
- **AI-Powered Analytics**: Personalized insights generated using LangChain
- **Visual Metrics**: 
  - Weekly accuracy trend charts (Chart.js)
  - Topic performance radar charts
  - Difficulty breakdown visualizations
- **Strength & Weakness Analysis**: AI identifies areas of excellence and improvement
- **Topic-Level Tracking**: Detailed performance data for each subject
- **Historical Trends**: Track improvement over time

---

## 🚀 Demo & Installation

### Prerequisites

- **Python 3.12+** (recommended) or 3.8+
- **Modern Web Browser** (Chrome, Firefox, Safari, Edge)
- **Groq API Key** - Get yours free at [console.groq.com](https://console.groq.com)

### Quick Start (5 Minutes)

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/mindmigo-ai-study-buddy.git
cd mindmigo-ai-study-buddy
```

#### 2. Set Up Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

#### 3. Install Dependencies

**Using `uv` (Recommended - Fast)**:
```bash
uv sync
```

**Using `pip`**:
```bash
pip install -e .
```

Dependencies include:
- FastAPI, Uvicorn (Backend framework)
- LangChain, LangChain-Groq (LLM orchestration)
- SQLAlchemy (Database ORM)
- PyVis (Graph visualization)
- Pandas (Data processing)

#### 4. Initialize the Database
```bash
python initialize_gamification_data.py
```

#### 5. Start the Backend Server
```bash
uvicorn main:app --reload
```

Backend will run at: `http://localhost:8000`  
API Docs available at: `http://localhost:8000/docs`

#### 6. Launch the Frontend

**Option A: Python HTTP Server (Recommended)**
```bash
cd frontend
python -m http.server 8080
```

**Option B: Node.js HTTP Server**
```bash
cd frontend
npx http-server -p 8080
```

**Option C: Direct File** (Limited functionality due to CORS)
```bash
# Simply open frontend/index.html in your browser
```

Frontend accessible at: `http://localhost:8080`

### Alternative: One-Click Start (Windows)
```bash
START_ALL.bat
```

This script automatically starts both backend and frontend servers.

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.118+ (High-performance async API framework)
- **AI/LLM**: 
  - LangChain 0.3+ (LLM orchestration framework)
  - LangChain-Groq (Groq API integration)
  - Groq LLaMA 3.1-8B-Instant (Primary language model)
- **Database**: SQLAlchemy 2.0+ with SQLite (Scalable to PostgreSQL)
- **Data Processing**: Pandas (Analytics and data manipulation)
- **Graph Generation**: PyVis 0.3+ (Interactive network visualizations)
- **API Server**: Uvicorn 0.37+ (ASGI server)

### Frontend
- **Core**: Vanilla JavaScript (ES6+), HTML5, CSS3
- **UI Framework**: Custom responsive design with CSS Grid/Flexbox
- **Charts**: Chart.js 4.4+ (Analytics visualizations)
- **Fonts**: Google Fonts (Inter)
- **Architecture**: Single Page Application (SPA) with dynamic routing

### DevOps & Tools
- **Package Manager**: uv (Modern Python packaging)
- **Build System**: Setuptools 61+
- **Version Control**: Git
- **Python Version**: 3.12+ (pyproject.toml configured)
- **Environment Management**: python-dotenv

### AI Pipeline
```
User Query → FastAPI Endpoint → Service Layer → LangChain → Groq API → LLaMA 3.1 → Response Processing → Frontend
```

---

## 📂 Project Structure

```
MindMigo-AI-Study-Buddy/
├── src/
│   ├── services/          # Business logic layer
│   │   ├── quiz_service.py
│   │   ├── knowledge_graph_service.py
│   │   ├── gamification_service.py
│   │   ├── progress_service.py
│   │   ├── chat_service.py
│   │   └── daily_problem_service.py
│   ├── generator/         # AI content generation
│   ├── database/          # SQLAlchemy models & DB
│   ├── models/            # Pydantic schemas
│   ├── prompts/           # LLM prompt templates
│   ├── config/            # Configuration files
│   ├── utils/             # Helper functions
│   └── common/            # Logging & exceptions
├── frontend/
│   ├── index.html         # Main SPA
│   ├── chat.html          # Embedded chat interface
│   ├── css/               # Stylesheets
│   │   ├── styles.css
│   │   ├── gamification.css
│   │   ├── progress.css
│   │   └── notifications.css
│   └── js/                # JavaScript modules
│       ├── api.js         # API client
│       ├── gamification.js
│       ├── quiz.js
│       ├── progress.js
│       └── main.js
├── main.py                # FastAPI application entry
├── pyproject.toml         # Project dependencies
├── .env                   # Environment variables
└── studdy_buddy.db        # SQLite database
```

---

## 🎮 How It Works

### 1. Quiz Generation Flow
```
User Input (Topic, Difficulty, Type) 
  → Quiz Service validates and processes
  → Question Generator calls Groq API with custom prompts
  → LangChain structures the LLM response
  → Duplicate prevention algorithm checks uniqueness
  → Response validated and returned as JSON
  → Frontend renders interactive quiz
  → Gamification Service awards XP on completion
```

### 2. Knowledge Graph Creation
```
User Input (Topic or Custom Text)
  → Knowledge Graph Service initiates generation
  → If topic provided: LLM generates explanatory content
  → Graph Extraction: Identifies nodes and relationships
  → PyVis renders HTML graph with physics simulation
  → Base64 encoded for safe transmission
  → Frontend displays in iframe with fullscreen option
  → XP awarded for graph creation
```

### 3. Gamification Engine
```
User Action (Quiz, Login, Daily Problem)
  → Gamification Service triggered
  → XP Transaction recorded in database
  → Level calculation based on total XP
  → Streak logic checks last activity date
  → Badge eligibility evaluation
  → Leaderboard position updated
  → Real-time UI updates via API
```

---

## 🌟 Unique Features & Innovation

1. **Adaptive Learning**: AI analyzes performance patterns to provide personalized feedback and recommendations
2. **Duplicate Prevention**: Advanced semantic similarity algorithms ensure quiz question diversity
3. **Gamification Integration**: Every learning action rewards students, maintaining motivation
4. **Progress Persistence**: All data stored in SQLite for seamless session continuity
5. **Modular Architecture**: Clean separation of concerns enables easy feature additions
6. **Zero Vendor Lock-in**: Can swap Groq for OpenAI, Anthropic, or any LangChain-compatible LLM
7. **Responsive Design**: Fully functional on desktop, tablet, and mobile devices

---

## 📈 Future Enhancements

### Short-Term (Post-Hackathon)
- [ ] **User Authentication**: Firebase or Auth0 integration for multi-user support
- [ ] **Export Functionality**: Download quizzes as PDF, share knowledge graphs as images
- [ ] **Enhanced AI Tutor**: Voice input/output, code execution environment for programming help
- [ ] **Social Features**: Study groups, collaborative knowledge graphs, friend challenges
- [ ] **Advanced Analytics**: Machine learning-based learning curve predictions

### Medium-Term
- [ ] **Mobile App**: React Native or Flutter mobile application
- [ ] **Content Library**: Pre-generated quiz templates, curated knowledge graphs
- [ ] **Teacher Dashboard**: Create custom quizzes, track student progress, assign homework
- [ ] **Multi-Language Support**: i18n implementation for global accessibility
- [ ] **Spaced Repetition**: AI-optimized review scheduling based on forgetting curves

### Long-Term Vision
- [ ] **AR/VR Integration**: Immersive 3D knowledge graph exploration
- [ ] **Adaptive Curriculum**: AI generates personalized learning paths
- [ ] **Video Content Analysis**: Generate quizzes from educational videos
- [ ] **Peer Tutoring Network**: Connect students for mutual learning
- [ ] **Institution Partnerships**: Integration with school LMS platforms (Canvas, Moodle)

---

## 👤 Team

**Solo Developer**: Satyam  
**Role**: Full-Stack Developer, AI Engineer  
**GitHub**: [@yourusername](https://github.com/yourusername)  
**Email**: satyampant420@example.com

---

## 🙏 Acknowledgments

- **Groq** for providing fast, free LLM API access
- **LangChain** community for excellent documentation
- **FastAPI** team for building an amazing framework
- **PyVis** for making graph visualization simple

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🐛 Known Issues & Solutions

| Issue | Solution |
|-------|----------|
| CORS errors in browser | Use Python/Node HTTP server instead of opening file directly |
| Port 8000 already in use | Change backend port: `uvicorn main:app --port 8001 --reload` |
| Knowledge graph not rendering | Verify backend is running, check browser console for errors |
| Quiz questions duplicating | Algorithm retries up to 5 times, rare edge case |

---

## 📞 Support & Contribution

Found a bug? Have a feature request? 

1. Open an issue on [GitHub Issues](https://github.com/yourusername/mindmigo-ai-study-buddy/issues)
2. Submit a pull request with improvements
3. Star ⭐ the repository if you find it useful!

---

## 🎓 Educational Impact

MindMigo addresses key challenges in modern education:

- **Accessibility**: Free AI-powered tutoring for all students
- **Engagement**: Gamification increases study time by an average of 40%
- **Personalization**: Adapts to individual learning speeds and styles
- **Retention**: Visual knowledge graphs improve concept retention by 60%
- **Motivation**: Streak systems and badges reduce dropout rates

---

**Built with ❤️ for learners everywhere. Happy Studying! 🚀📚**
