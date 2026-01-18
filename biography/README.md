# Biography RAG System

A full-stack **Retrieval-Augmented Generation (RAG)** application that allows you to upload a biography and interact with it through an AI-powered chatbot. The system uses Google's Gemini AI to answer questions as if it were the person in the biography.

## Features

- 📄 **Upload Biography** - Upload `.txt` files containing biographical information
- 💬 **Interactive Chat** - Ask questions and get answers from the AI representing the person
- 🔒 **Rate Limiting** - Built-in protection against API quota exhaustion
  - 10 requests per minute (RPM)
  - 250 requests per day (RPD)
- 📊 **Usage Tracking** - Monitor your API usage in real-time
- 🔄 **Retry Logic** - Automatic retry with exponential backoff for failed requests
- 🎨 **Modern UI** - Clean, responsive React frontend

## Tech Stack

### Backend (FastAPI)

- **FastAPI** - High-performance Python web framework
- **LangChain** - RAG pipeline orchestration
- **Google Gemini AI** - LLM for embeddings and chat
- **FAISS** - Vector store for semantic search
- **Pydantic** - Data validation

### Frontend (React)

- **React** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Fetch API** - HTTP client

## Project Structure

```
biography/
├── app.py                 # FastAPI backend server
└── rag-biography/         # React frontend
    ├── src/
    │   ├── App.jsx        # Main application component
    │   └── ...
    ├── package.json
    └── vite.config.js
```

## Setup

### Prerequisites

- Python 3.10+
- Node.js 16+
- Google Gemini API key

### Backend Setup

1. **Navigate to the biography folder:**

   ```bash
   cd biography
   ```

2. **Create and activate virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install fastapi uvicorn langchain langchain-google-genai langchain-community faiss-cpu python-multipart
   ```

4. **Create `.env` file:**

   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

5. **Run the backend:**
   ```bash
   python app.py
   ```
   Backend will run on `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend folder:**

   ```bash
   cd rag-biography
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```
   Frontend will run on `http://localhost:5173`

## Usage

### 1. Upload a Biography

1. Open the application in your browser (`http://localhost:5173`)
2. Enter your Google Gemini API key
3. Click "Upload Biography" and select a `.txt` file
4. Wait for processing (creates vector embeddings)

### 2. Ask Questions

Once uploaded, you can ask questions like:

- "What is your background?"
- "Tell me about your education"
- "What are your achievements?"
- "What inspired you to pursue your career?"

The AI will respond as if it were the person in the biography!

### 3. Monitor Usage

The UI displays:

- Requests per minute (RPM) used/remaining
- Requests per day (RPD) used/remaining
- Real-time usage updates after each query

## API Endpoints

### `POST /upload`

Upload a biography file and create a vector store.

**Request:**

- `file`: Biography text file (`.txt`)
- `api_key`: Google Gemini API key

**Response:**

```json
{
  "session_id": "uuid",
  "message": "Biography processed successfully",
  "usage": {
    "rpm_used": 1,
    "rpm_limit": 10,
    "rpd_used": 1,
    "rpd_limit": 250
  }
}
```

### `POST /query`

Ask a question about the biography.

**Request:**

```json
{
  "session_id": "uuid",
  "question": "What is your background?",
  "api_key": "your_api_key"
}
```

**Response:**

```json
{
  "answer": "I am...",
  "session_id": "uuid",
  "usage": {...}
}
```

### `GET /usage/{api_key}`

Get current usage statistics.

**Response:**

```json
{
  "rpm_used": 5,
  "rpm_limit": 10,
  "rpd_used": 50,
  "rpd_limit": 250,
  "rpm_remaining": 5,
  "rpd_remaining": 200
}
```

### `DELETE /session/{session_id}`

Delete a session and free resources.

### `GET /health`

Health check endpoint.

## Rate Limiting

The system implements intelligent rate limiting to protect against API quota exhaustion:

### Limits

- **RPM (Requests Per Minute):** 10
- **RPD (Requests Per Day):** 250

### Behavior

- Tracks requests per API key
- Automatically resets daily counters after 24 hours
- Returns `429` status code when limits exceeded
- Provides wait time for RPM limits

### Error Handling

- Automatic retry with exponential backoff (3 attempts)
- Graceful degradation on quota errors
- User-friendly error messages

## How It Works

### RAG Pipeline

1. **Document Processing**

   - Biography text is split into chunks (1000 chars, 200 overlap)
   - Each chunk is embedded using Google's `text-embedding-004` model

2. **Vector Storage**

   - Embeddings stored in FAISS vector database
   - Enables fast semantic similarity search

3. **Query Processing**

   - User question is embedded
   - Top relevant chunks retrieved via similarity search
   - Context + question sent to Gemini LLM

4. **Response Generation**
   - LLM generates answer as if it were the person
   - Cites only information from the biography
   - Says "I don't know" if answer not in context

## Configuration

### Backend (`app.py`)

```python
# Rate limits
RPM_LIMIT = 10   # Requests per minute
RPD_LIMIT = 250  # Requests per day

# Text splitting
chunk_size = 1000
chunk_overlap = 200

# LLM model
model = "gemini-2.0-flash-exp"
temperature = 0.3
```

### Frontend

Update API base URL in `src/App.jsx` if needed:

```javascript
const API_BASE_URL = "http://localhost:8000";
```

## Troubleshooting

### Backend Issues

**"Rate limit exceeded"**

- Wait for the specified time (shown in error message)
- Check usage with `/usage/{api_key}` endpoint

**"Vector store creation failed"**

- Ensure API key is valid
- Check file is UTF-8 encoded
- Verify file is `.txt` format

### Frontend Issues

**CORS errors**

- Ensure backend is running on port 8000
- Check CORS middleware is enabled in `app.py`

**Upload fails**

- Check file size (large files may timeout)
- Verify API key is correct
- Check browser console for errors

## Development

### Running Tests

```bash
# Backend
pytest

# Frontend
npm test
```

### Building for Production

**Frontend:**

```bash
cd rag-biography
npm run build
```

**Backend:**

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Future Enhancements

- [ ] Support for PDF and DOCX files
- [ ] Multi-language support
- [ ] Conversation history
- [ ] Export chat transcripts
- [ ] User authentication
- [ ] Persistent storage (database)
- [ ] Deployment guides (Docker, cloud platforms)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [Google Gemini AI](https://ai.google.dev/)
- UI inspired by modern chat interfaces
