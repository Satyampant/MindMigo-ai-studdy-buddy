# Studdy Buddy AI - Complete Setup Guide

This guide will help you set up both the backend and frontend for the Studdy Buddy AI application.

## Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, or Edge)
- Groq API key (get from https://console.groq.com)

## Backend Setup

### 1. Navigate to Project Directory

```bash
cd "C:\Users\pheno\Gen AI Projects\LLMOps and AIOps\Studdy Buddy AI"
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root with your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Install Dependencies

If using `uv`:
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

### 4. Start the Backend Server

```bash
uvicorn main:app --reload
```

The backend will be available at: `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Frontend Setup

### Option 1: Direct File Opening (Simplest)

1. Navigate to the frontend directory
2. Open `index.html` directly in your web browser

**Note**: Some features may not work due to CORS restrictions. Use Option 2 for full functionality.

### Option 2: Using Python HTTP Server (Recommended)

```bash
cd frontend
python -m http.server 8080
```

Access at: `http://localhost:8080`

### Option 3: Using Node.js http-server

```bash
cd frontend
npx http-server -p 8080
```

Access at: `http://localhost:8080`

## Verification

### Backend Health Check

Visit `http://localhost:8000/` - you should see:
```json
{
  "message": "🤖 Studdy Buddy AI Backend is running! Navigate to /docs for API documentation."
}
```

### Frontend Connection Check

1. Open the frontend in your browser
2. Open browser console (F12)
3. You should see: "✅ Connected to backend successfully"

## Testing the Application

### 1. Test Quiz Generator

1. Navigate to "Quiz Generator"
2. Enter topic: "Python programming"
3. Select: Multiple Choice, Medium difficulty, 3 questions
4. Click "Generate Quiz"
5. Verify questions appear correctly

### 2. Test Knowledge Graph

1. Navigate to "Knowledge Graph"
2. Enter topic: "Machine Learning"
3. Click "Generate Knowledge Graph"
4. Verify the interactive graph displays
5. Try "View Fullscreen" button

### 3. Test Daily Challenge

1. Navigate to "Daily Challenge"
2. Wait for problem to load
3. Select an answer
4. Click "Submit Answer"
5. Verify feedback appears
6. Check stats update correctly

## Troubleshooting

### Backend Issues

**Problem**: `GROQ_API_KEY environment variable is not set`
- Solution: Ensure `.env` file exists with valid API key

**Problem**: `ModuleNotFoundError`
- Solution: Install all dependencies: `pip install -r requirements.txt`

**Problem**: Port 8000 already in use
- Solution: Use different port: `uvicorn main:app --port 8001 --reload`
- Update `CONFIG.API_BASE_URL` in `frontend/js/config.js`

### Frontend Issues

**Problem**: "Cannot connect to backend"
- Solution: Ensure backend is running on correct port
- Check `frontend/js/config.js` has correct API URL

**Problem**: Knowledge graph not displaying
- Solution: Check browser console for errors
- Verify backend returned base64 encoded content
- Clear browser cache and reload

**Problem**: CORS errors
- Solution: Use a local server (Option 2 or 3) instead of opening file directly
- Backend already has CORS enabled for development

### Common Fixes

**Clear browser cache**:
- Chrome: Ctrl+Shift+Delete
- Firefox: Ctrl+Shift+Delete
- Safari: Cmd+Option+E

**Reset local storage** (if stats aren't working):
```javascript
// Open browser console and run:
localStorage.clear();
```

**Restart backend with clean state**:
```bash
# Stop server (Ctrl+C)
# Start again
uvicorn main:app --reload
```

## Configuration

### Backend Configuration

Edit `src/config/settings.py`:

```python
MODEL_NAME = "llama-3.1-8b-instant"  # Change model
TEMPERATURE = 0.9                     # Adjust creativity
MAX_RETRIES = 3                       # API retry attempts
```

### Frontend Configuration

Edit `frontend/js/config.js`:

```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',  // Backend URL
    TOAST_DURATION: 5000,                    // Notification duration (ms)
    ...
};
```

## Production Deployment

### Backend

1. Set production environment variables
2. Disable debug mode
3. Use production ASGI server (e.g., Gunicorn with Uvicorn workers)
4. Configure proper CORS origins in `main.py`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Frontend

1. Build/minify assets if needed
2. Update `API_BASE_URL` in `config.js` to production URL
3. Deploy to static hosting (Netlify, Vercel, S3, etc.)

## Features Implemented

✅ Quiz Generation (MCQ and Fill in the Blank)
✅ Knowledge Graph Visualization
✅ Daily Challenge System
✅ Progress Tracking (Streak, Accuracy, Problems Solved)
✅ Responsive Design (Desktop, Tablet, Mobile)
✅ Toast Notifications
✅ Loading States
✅ Error Handling
✅ Local Storage Persistence

## Known Issues & Solutions

1. **Dual 200/422 responses**: Fixed by disabling streaming in `groq_client.py`
2. **JSON decode error**: Fixed by base64 encoding HTML in `generate_knowledge_graph.py`
3. **CORS issues**: Fixed by enabling CORS middleware in `main.py`

## Support

For issues or questions:
1. Check browser console for errors
2. Check backend logs for API errors
3. Verify all dependencies are installed
4. Ensure API key is valid and has credits

## Next Steps

- Customize the UI in `frontend/css/styles.css`
- Add more question types
- Implement user authentication
- Add export functionality for quizzes
- Create mobile app version

---

**Happy Learning with Studdy Buddy AI! 🤖📚**
