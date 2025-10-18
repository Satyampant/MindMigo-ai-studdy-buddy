from langchain_groq import ChatGroq
from src.config.settings import settings
from src.common.logger import get_logger

class FeedbackGenerator:
    def __init__(self):
        self.llm = ChatGroq(model=settings.MODEL_NAME, temperature=0.7, groq_api_key=settings.GROQ_API_KEY)
        self.logger = get_logger(self.__class__.__name__)

    async def generate_strength_feedback(self, strongest_topic: str, accuracy: float, attempts: int) -> str:
        prompt = f"""You are an encouraging AI tutor. A student has shown strength in {strongest_topic} with {accuracy}% accuracy over {attempts} attempts.

Provide 2-3 sentences of encouraging feedback that:
1. Celebrates their achievement
2. Suggests ways to maintain or deepen this strength
3. Keeps a warm, motivational tone

Feedback:"""
        
        response = await self.llm.ainvoke(prompt)
        return response.content.strip()

    async def generate_weakness_feedback(self, weakest_topic: str, accuracy: float, attempts: int) -> str:
        prompt = f"""You are a supportive AI tutor. A student needs improvement in {weakest_topic} with {accuracy}% accuracy over {attempts} attempts.

Provide 2-3 sentences of constructive feedback that:
1. Acknowledges the challenge without discouragement
2. Offers specific, actionable practice recommendations
3. Maintains an encouraging, supportive tone

Feedback:"""
        
        response = await self.llm.ainvoke(prompt)
        return response.content.strip()

    async def generate_overall_insight(self, overall_accuracy: float, total_attempts: int, topics: list) -> str:
        topics_summary = ", ".join([f"{t['topic']} ({t['accuracy']}%)" for t in topics[:3]])
        
        prompt = f"""You are an insightful AI learning coach. Review this student's progress:
- Overall Accuracy: {overall_accuracy}%
- Total Quizzes: {total_attempts}
- Topic Performance: {topics_summary}

Provide 2-3 sentences that:
1. Summarize their learning journey
2. Highlight patterns or trends
3. Suggest next steps for improvement

Insight:"""
        
        response = await self.llm.ainvoke(prompt)
        return response.content.strip()
