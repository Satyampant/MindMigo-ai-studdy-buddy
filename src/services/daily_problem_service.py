from src.generator.question_generator import QuestionGenerator
from src.models.api_schemas import DailyProblemResponse
from src.models.question_schemas import MCQQuestion
from src.common.logger import get_logger

class DailyProblemService:
    def __init__(self):
        self.generator = QuestionGenerator()
        self.logger = get_logger(self.__class__.__name__)
        self.default_topic = "Python programming"
        self.default_difficulty = "hard"

    def _format_mcq_response(self, mcq_q: MCQQuestion) -> DailyProblemResponse:
        return DailyProblemResponse(
            question_type="MCQ",
            topic=self.default_topic,
            difficulty=self.default_difficulty,
            question=mcq_q.question,
            options=mcq_q.options,
            correct_answer=mcq_q.correct_answer
        )

    # In a production app, this would implement caching to serve the same question for 24h.
    async def get_daily_problem(self) -> DailyProblemResponse:
        """Generates a challenging daily MCQ problem (hardcoded to Python/hard)."""
        self.logger.info(f"Generating daily problem for topic: {self.default_topic}, difficulty: {self.default_difficulty}")
        
        # Await the asynchronous generator call
        mcq_q = await self.generator.generate_mcq(self.default_topic, self.default_difficulty)
        
        return self._format_mcq_response(mcq_q)