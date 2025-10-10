from typing import List
from src.generator.question_generator import QuestionGenerator
from src.models.api_schemas import QuizQuestion, QuizResponse, QuizSettings
from src.common.custom_exception import CustomException
from src.common.logger import get_logger
import asyncio

class QuizService:
    def __init__(self):
        self.generator = QuestionGenerator()
        self.logger = get_logger(self.__class__.__name__)

    async def generate_questions(self, settings: QuizSettings) -> QuizResponse:
        questions: List[QuizQuestion] = []
        question_type = settings.question_type
        topic = settings.topic
        difficulty = settings.difficulty
        num_questions = settings.num_questions

        # Create concurrent tasks for efficient generation
        generation_tasks = []
        for _ in range(num_questions):
            if question_type == "Multiple Choice":
                task = self.generator.generate_mcq(topic, difficulty.lower())
            elif question_type == "Fill in the blank":
                task = self.generator.generate_fill_blank(topic, difficulty.lower())
            else:
                 # Should not happen if validation is correct, but safe to handle
                 continue 
            generation_tasks.append(task)

        # Wait for all tasks to complete, allowing exceptions for individual failures
        results = await asyncio.gather(*generation_tasks, return_exceptions=True)

        for idx, result in enumerate(results):
            if isinstance(result, Exception):
                # Log the failure but continue processing other successfully generated questions
                self.logger.warning(f"Skipping failed question {idx + 1}/{num_questions}: {str(result)}")
                continue

            # Format the successfully generated question for the API response
            if question_type == "Multiple Choice":
                questions.append(
                    QuizQuestion(
                        type='MCQ',
                        question=result.question,
                        options=result.options,
                        correct_answer=result.correct_answer
                    )
                )

            elif question_type == "Fill in the blank":
                questions.append(
                    QuizQuestion(
                        type='Fill in the blank',
                        question=result.question,
                        correct_answer=result.answer
                    )
                )
        
        if not questions:
            raise CustomException(
                f"Failed to generate any questions for topic '{topic}' with difficulty '{difficulty}' "
                f"and question type '{question_type}' after multiple attempts."
            )

        return QuizResponse(questions=questions)