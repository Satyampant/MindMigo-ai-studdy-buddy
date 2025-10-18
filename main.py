from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.models.api_schemas import QuizSettings, QuizResponse, KnowledgeGraphRequest, KnowledgeGraphResponse, DailyProblemResponse, ChatRequest, ChatResponse
from src.models.progress_schemas import QuizAttemptRequest, QuizAttemptResponse, AnalyticsResponse
from src.models.gamification_schemas import GamificationProfile, LeaderboardResponse, LeaderboardEntry, BadgeResponse, XPTransactionResponse
from src.services.quiz_service import QuizService
from src.services.knowledge_graph_service import KnowledgeGraphService
from src.services.daily_problem_service import DailyProblemService
from src.services.progress_service import ProgressService
from src.services.chat_service import ChatService
from src.services.gamification_service import GamificationService
from src.database.database import get_db, init_db
from src.common.custom_exception import CustomException
from src.common.logger import get_logger
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

app = FastAPI(title="Studdy Buddy AI Backend", description="Backend services for Quiz Generation, Knowledge Graph, and Daily Problem.", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
init_db()

quiz_service = QuizService()
kg_service = KnowledgeGraphService()
daily_problem_service = DailyProblemService()
progress_service = ProgressService()
chat_service = ChatService()
gamification_service = GamificationService()
logger = get_logger("FastAPI_Main")

async def _handle_service_call(coro):
    try:
        return await coro
    except CustomException as e:
        logger.error(f"Service Error: {e.error_message}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e.error_message))
    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred in the service.")

@app.get("/", summary="Root Health Check")
async def read_root():
    return {"message": "🤖 Studdy Buddy AI Backend is running! Navigate to /docs for API documentation."}

@app.post("/quiz/generate", response_model=QuizResponse, summary="Generate a Quiz")
async def generate_quiz_endpoint(settings: QuizSettings):
    logger.info(f"Generating quiz with settings: {settings.model_dump()}")
    return await _handle_service_call(quiz_service.generate_questions(settings))

@app.post("/knowledge-graph/generate", response_model=KnowledgeGraphResponse, summary="Generate Knowledge Graph (HTML)")
async def generate_knowledge_graph_endpoint(request: KnowledgeGraphRequest, student_id: str = None, db: Session = Depends(get_db)):
    if not request.text and not request.topic:
        raise HTTPException(status_code=400, detail="Must provide either 'text' or 'topic'.")
    result = await _handle_service_call(kg_service.create_knowledge_graph(request))
    if student_id:
        try:
            gamification_service.award_xp(db, student_id, "graph_creation", f"Created graph for {request.topic or 'custom text'}")
            gamification_service.check_and_award_badges(db, student_id)
        except Exception:
            pass
    return result

@app.post("/knowledge-graph/render", summary="Render Knowledge Graph HTML for testing")
async def render_knowledge_graph_html(request: KnowledgeGraphRequest):
    response = await _handle_service_call(kg_service.create_knowledge_graph(request))
    return HTMLResponse(content=response.html_content)

@app.get("/daily-problem", response_model=DailyProblemResponse, summary="Get the Daily Challenging Problem")
async def get_daily_problem_endpoint():
    return await _handle_service_call(daily_problem_service.get_daily_problem())

@app.post("/daily-problem/submit", summary="Submit Daily Problem Answer")
def submit_daily_problem(student_id: str, is_correct: bool, db: Session = Depends(get_db)):
    try:
        if is_correct:
            gamification_service.award_xp(db, student_id, "daily_problem", "Solved daily problem")
        gamification_service.update_streak(db, student_id)
        gamification_service.check_and_award_badges(db, student_id)
        return {"success": True, "message": "Daily problem recorded"}
    except Exception as e:
        logger.error(f"Failed to record daily problem: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/progress/record", response_model=QuizAttemptResponse, summary="Record Quiz Attempt")
def record_progress_endpoint(attempt: QuizAttemptRequest, db: Session = Depends(get_db)):
    try:
        result = progress_service.record_quiz_attempt(db, attempt)
        logger.info(f"Recorded quiz attempt for student {attempt.student_id}: {result['accuracy']}% accuracy")
        gamification_service.award_xp(db, attempt.student_id, "quiz_completion", f"Completed quiz: {attempt.topic}")
        if result['accuracy'] == 100:
            gamification_service.award_xp(db, attempt.student_id, "perfect_quiz", "Perfect score on quiz!")
        gamification_service.update_streak(db, attempt.student_id)
        gamification_service.check_and_award_badges(db, attempt.student_id)
        return result
    except Exception as e:
        logger.error(f"Failed to record progress: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/progress/analytics/{student_id}", response_model=AnalyticsResponse, summary="Get Student Analytics")
def get_analytics_endpoint(student_id: str, db: Session = Depends(get_db)):
    try:
        result = progress_service.get_student_analytics(db, student_id)
        logger.info(f"Retrieved analytics for student {student_id}: {result['overall_accuracy']}% overall")
        return result
    except Exception as e:
        logger.error(f"Failed to retrieve analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/progress/analytics/{student_id}/ai", response_model=AnalyticsResponse, summary="Get Student Analytics with AI Feedback")
async def get_analytics_with_ai_endpoint(student_id: str, db: Session = Depends(get_db)):
    try:
        result = await progress_service.get_student_analytics_with_ai_feedback(db, student_id)
        logger.info(f"Retrieved AI-enhanced analytics for student {student_id}")
        return result
    except Exception as e:
        logger.error(f"Failed to retrieve AI analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/message", response_model=ChatResponse, summary="Send Message to AI Tutor")
async def chat_message_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    conv_id = chat_service.create_or_get_conversation(db, request.student_id, request.conversation_id)
    chat_service.add_message_to_history(db, conv_id, "student", request.message)
    tutor_reply = await chat_service.get_tutor_response(db, conv_id, request.message)
    chat_service.add_message_to_history(db, conv_id, "tutor", tutor_reply)
    history = chat_service.format_conversation_context(db, conv_id)
    return ChatResponse(reply=tutor_reply, conversation_id=conv_id, message_history=history)

@app.get("/chat/history/{conversation_id}", response_model=ChatResponse, summary="Get Conversation History")
async def get_chat_history_endpoint(conversation_id: str, db: Session = Depends(get_db)):
    history = chat_service.format_conversation_context(db, conversation_id)
    return ChatResponse(reply="", conversation_id=conversation_id, message_history=history)

@app.post("/auth/login", summary="Track Daily Login and Update Streak")
def daily_login_endpoint(student_id: str, db: Session = Depends(get_db)):
    try:
        gamification_service.get_or_create_profile(db, student_id)
        streak_result = gamification_service.update_streak(db, student_id)
        if streak_result["streak_status"] != "already_counted":
            gamification_service.award_xp(db, student_id, "daily_login", "Daily Login Bonus")
        return {"success": True, "streak": streak_result, "message": f"Welcome back! Current streak: {streak_result['current_streak']} days"}
    except Exception as e:
        logger.error(f"Failed to track login: {str(e)}")
        return {"success": False, "message": "Login tracked but gamification update failed"}

@app.get("/gamification/{student_id}", response_model=GamificationProfile, summary="Get Student Gamification Profile")
def get_gamification_profile(student_id: str, db: Session = Depends(get_db)):
    try:
        from src.config.gamification_config import BADGE_DEFINITIONS, get_xp_for_next_level, get_level_progress_percentage
        gamification_service.get_or_create_profile(db, student_id)
        profile = gamification_service.get_student_gamification(db, student_id)
        badges = [BadgeResponse(badge_id=b["badge_id"], badge_name=BADGE_DEFINITIONS.get(b["badge_id"], {}).get("name", b["badge_id"]), badge_type=b["badge_type"], description=BADGE_DEFINITIONS.get(b["badge_id"], {}).get("description", ""), earned_date=b["earned_date"]) for b in profile["badges"]]
        transactions = [XPTransactionResponse(**t) for t in profile["recent_transactions"]]
        return GamificationProfile(**{**profile, "badges": badges, "recent_transactions": transactions, "xp_for_next_level": get_xp_for_next_level(profile["total_xp"]), "level_progress_percentage": get_level_progress_percentage(profile["total_xp"])})
    except Exception as e:
        logger.error(f"Failed to get gamification profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/leaderboard", response_model=LeaderboardResponse, summary="Get Leaderboard")
def get_leaderboard(limit: int = 10, student_id: str = None, db: Session = Depends(get_db)):
    try:
        from src.database.models import StudentGamification
        if student_id:
            gamification_service.get_or_create_profile(db, student_id)
        all_students = db.query(StudentGamification).order_by(StudentGamification.total_xp.desc()).all()
        if not all_students:
            return LeaderboardResponse(entries=[], total_students=0, current_user_rank=None)
        top_students = all_students[:limit]
        entries = [LeaderboardEntry(rank=idx+1, student_id=s.student_id, display_name=f"Student {s.student_id[-8:]}", total_xp=s.total_xp, level=s.level, badge_count=len(s.badges), is_current_user=(s.student_id == student_id)) for idx, s in enumerate(top_students)]
        current_rank = next((idx+1 for idx, s in enumerate(all_students) if s.student_id == student_id), None) if student_id else None
        logger.info(f"Retrieved leaderboard with {len(entries)} entries")
        return LeaderboardResponse(entries=entries, total_students=len(all_students), current_user_rank=current_rank)
    except Exception as e:
        logger.error(f"Failed to get leaderboard: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
