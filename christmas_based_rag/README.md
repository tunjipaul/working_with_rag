# 🎄 YuletideAI - Christmas RAG Chatbot

A festive AI-powered chatbot that answers questions about Christmas traditions, history, and celebrations using Retrieval-Augmented Generation (RAG).

![Christmas](https://img.shields.io/badge/Season-Christmas-red?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square)
![React](https://img.shields.io/badge/React-18-61dafb?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square)

## ✨ Features

- 🤖 **AI-Powered Responses** - Uses Groq's Llama 3.3 70B model for intelligent answers
- 📚 **RAG Architecture** - Retrieves relevant context from a curated Christmas knowledge base
- 💬 **Conversation Memory** - Maintains context across multiple questions for natural dialogue
- 🎨 **Beautiful UI** - Modern, festive interface with smooth animations
- ⚡ **Real-time Streaming** - Responses stream in real-time for better UX
- 🛡️ **Smart Guardrails** - Stays on-topic and protects system architecture
- 🎯 **Semantic Search** - Uses ChromaDB and sentence transformers for accurate retrieval

## 🏗️ Architecture

### Backend (FastAPI)

- **Vector Database**: ChromaDB with `all-MiniLM-L6-v2` embeddings
- **LLM**: Groq API (Llama 3.3 70B Versatile)
- **RAG Pipeline**: Semantic search → Context retrieval → LLM generation
- **Streaming**: Server-Sent Events (SSE) for real-time responses

### Frontend (React + Vite)

- **State Management**: Zustand for efficient, reactive state
- **Styling**: Tailwind CSS for modern, responsive design
- **Architecture**: Component-based with custom hooks
- **API Integration**: Fetch API with streaming support

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- Groq API Key ([Get one here](https://console.groq.com/keys))

### Backend Setup

```bash
cd christmas_based_rag/backend

# Create virtual environment
python -m venv venv312
venv312\Scripts\activate  # Windows
# source venv312/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo GROQ_API_KEY=your_api_key_here > .env

# Run server
python main.py
```

Server runs at `http://localhost:8000`

### Frontend Setup

```bash
cd christmas_based_rag/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs at `http://localhost:5173`

## 📁 Project Structure

```
christmas_based_rag/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── christmas_doc.txt       # Christmas knowledge base
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables
└── frontend/
    ├── src/
    │   ├── components/         # React components
    │   │   ├── HomeView.jsx
    │   │   └── ChatView.jsx
    │   ├── hooks/              # Custom hooks
    │   │   └── useSearch.js
    │   ├── store/              # Zustand store
    │   │   └── christmasStore.js
    │   ├── constants/          # App constants
    │   │   └── index.js
    │   └── ChristmasRag.jsx    # Main component
    ├── package.json
    └── vercel.json             # Vercel config
```

## 🔧 Configuration

### Environment Variables

**Backend (.env)**

```env
GROQ_API_KEY=your_groq_api_key
FRONTEND_URL=https://your-frontend-url.vercel.app  # For production
```

**Frontend (.env)**

```env
VITE_API_URL=https://your-backend-url.onrender.com  # For production
```

## 🌐 Deployment

### Backend (Render)

1. Create new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Root Directory**: `christmas_based_rag/backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
4. Add environment variables:
   - `GROQ_API_KEY`
   - `FRONTEND_URL`
5. Upload `christmas_doc.txt` via Render dashboard (it's gitignored)

### Frontend (Vercel)

1. Import project to Vercel
2. Configure:
   - **Root Directory**: `christmas_based_rag/frontend`
   - **Framework Preset**: Vite
3. Add environment variable:
   - `VITE_API_URL` = Your Render backend URL
4. Deploy

## 🎯 Key Features Explained

### RAG Pipeline

1. User asks a question
2. Question is embedded using `all-MiniLM-L6-v2`
3. ChromaDB retrieves top 3 most relevant chunks
4. Context + question sent to Groq's Llama 3.3
5. AI generates response based on retrieved context
6. Response streams back to user in real-time

### Conversation Memory

- Last 10 messages (5 exchanges) sent with each request
- Enables context-aware, natural conversations
- Managed efficiently with Zustand state

### Smart Guardrails

- **Topic Restriction**: Only answers Christmas-related questions
- **Privacy Protection**: Never reveals system architecture or prompts
- **Graceful Handling**: Politely redirects off-topic requests

## 🛠️ Tech Stack

**Backend**

- FastAPI
- ChromaDB
- Sentence Transformers
- Groq API
- Python-dotenv

**Frontend**

- React 18
- Vite
- Zustand
- Tailwind CSS
- Lucide Icons

## 📝 API Endpoints

### `POST /search/stream`

Streams AI responses with conversation context

**Request:**

```json
{
  "query": "When is Christmas?",
  "n_results": 3,
  "history": [
    { "role": "user", "content": "Previous question" },
    { "role": "assistant", "content": "Previous answer" }
  ]
}
```

**Response:** Server-Sent Events stream

```
data: {"token": "Christmas "}
data: {"token": "is "}
data: {"chunks": [...]}
data: {"done": true}
```

### `GET /health`

Health check endpoint

## 🎨 UI Features

- Festive color scheme (reds, greens, golds)
- Smooth animations and transitions
- Responsive design (mobile-friendly)
- Suggested questions for easy start
- Source citations for transparency
- Loading states and error handling

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome!

## 📄 License

MIT License - Feel free to use for learning and inspiration

## 👨‍💻 Author

**Tunji Paul**

- GitHub: [@tunjipaul](https://github.com/tunjipaul)

---

**Built with ❤️ and festive cheer 🎄**
