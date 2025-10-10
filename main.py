from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.models.api_schemas import QuizSettings, QuizResponse, KnowledgeGraphRequest, KnowledgeGraphResponse, DailyProblemResponse
from src.services.quiz_service import QuizService
from src.services.knowledge_graph_service import KnowledgeGraphService
from src.services.daily_problem_service import DailyProblemService
from src.common.custom_exception import CustomException
from src.common.logger import get_logger
from fastapi.responses import HTMLResponse

# Initialize FastAPI app
app = FastAPI(
    title="Studdy Buddy AI Backend",
    description="Backend services for Quiz Generation, Knowledge Graph, and Daily Problem.",
    version="1.0.0"
)

# Configure CORS (Important for separate frontend)
app.add_middleware(
    CORSMiddleware,
    # Allow all origins for development. Restrict this in production.
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
quiz_service = QuizService()
kg_service = KnowledgeGraphService()
daily_problem_service = DailyProblemService()
logger = get_logger("FastAPI_Main")

# --- Error Handling Helper ---
async def _handle_service_call(coro):
    try:
        result = await coro
        return result
    except CustomException as e:
        logger.error(f"Service Error: {e.error_message}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e.error_message))
    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred in the service.")

# --- API Endpoints ---

@app.get("/", summary="Root Health Check")
async def read_root():
    """Returns a simple status message."""
    return {"message": "🤖 Studdy Buddy AI Backend is running! Navigate to /docs for API documentation."}

# Service 1: Quiz Generator

@app.post("/quiz/generate", response_model=QuizResponse, summary="Generate a Quiz")
async def generate_quiz_endpoint(settings: QuizSettings):
    """Generates a list of quiz questions (MCQ or Fill in the blank) based on the provided settings."""
    logger.info(f"Generating quiz with settings: {settings.model_dump()}")
    return await _handle_service_call(quiz_service.generate_questions(settings))

# Service 2: Knowledge Graph Generator

@app.post("/knowledge-graph/generate", response_model=KnowledgeGraphResponse, summary="Generate Knowledge Graph (HTML)")
async def generate_knowledge_graph_endpoint(request: KnowledgeGraphRequest):
    """
    Generates a PyVis Knowledge Graph HTML string. 
    Provide 'text' to analyze directly, or provide only 'topic' to generate content first.
    """
    if not request.text and not request.topic:
        raise HTTPException(status_code=400, detail="Must provide either 'text' or 'topic'.")

    return await _handle_service_call(kg_service.create_knowledge_graph(request))
    
# Example endpoint for the frontend to render the HTML content directly
@app.post("/knowledge-graph/render", summary="Render Knowledge Graph HTML for testing")
async def render_knowledge_graph_html(request: KnowledgeGraphRequest):
    """A helper endpoint to test rendering of the HTML content directly in a browser."""
    response = await _handle_service_call(kg_service.create_knowledge_graph(request))
    return HTMLResponse(content=response.html_content)


# Service 3: Daily Problem

@app.get("/daily-problem", response_model=DailyProblemResponse, summary="Get the Daily Challenging Problem")
async def get_daily_problem_endpoint():
    """Retrieves a challenging question (Hard MCQ) on a default topic (Python programming)."""
    return await _handle_service_call(daily_problem_service.get_daily_problem())


# To run the application: 
# 1. Install dependencies: pip install fastapi uvicorn[standard] python-multipart
# 2. Run: uvicorn main:app --reload