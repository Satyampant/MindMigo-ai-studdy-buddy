from typing import List
from src.generator.question_generator import QuestionGenerator
from src.models.api_schemas import QuizQuestion, QuizResponse, QuizSettings
from src.common.custom_exception import CustomException
from src.common.logger import get_logger

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
        
        generated_questions_text = []  # Keep as list to maintain order
        max_attempts_per_question = 5

        for i in range(num_questions):
            question_generated = False
            
            for attempt in range(max_attempts_per_question):
                try:
                    # Pass previous questions for context
                    previous_questions = generated_questions_text.copy()
                    
                    if question_type == "Multiple Choice":
                        result = await self.generator.generate_mcq(
                            topic, 
                            difficulty.lower(),
                            previous_questions=previous_questions if previous_questions else None
                        )
                        
                        # Check for exact duplicate
                        if result.question not in generated_questions_text:
                            # Check for semantic similarity (basic check)
                            is_too_similar = False
                            question_lower = result.question.lower().strip()
                            
                            for prev_q in generated_questions_text:
                                prev_q_lower = prev_q.lower().strip()
                                # Calculate basic similarity
                                if self._are_questions_too_similar(question_lower, prev_q_lower):
                                    is_too_similar = True
                                    self.logger.warning(f"Question too similar to existing: '{result.question}' vs '{prev_q}'")
                                    break
                            
                            if not is_too_similar:
                                questions.append(
                                    QuizQuestion(
                                        type='MCQ',
                                        question=result.question,
                                        options=result.options,
                                        correct_answer=result.correct_answer
                                    )
                                )
                                generated_questions_text.append(result.question)
                                question_generated = True
                                self.logger.info(f"Generated unique question {i + 1}/{num_questions}")
                                break
                            else:
                                self.logger.warning(f"Semantically similar question detected, retrying... (attempt {attempt + 1})")
                        else:
                            self.logger.warning(f"Exact duplicate question detected, retrying... (attempt {attempt + 1})")
                    
                    elif question_type == "Fill in the blank":
                        result = await self.generator.generate_fill_blank(
                            topic,
                            difficulty.lower(),
                            previous_questions=previous_questions if previous_questions else None
                        )
                        
                        # Check for exact duplicate
                        if result.question not in generated_questions_text:
                            # Check for semantic similarity
                            is_too_similar = False
                            question_lower = result.question.lower().strip()
                            
                            for prev_q in generated_questions_text:
                                prev_q_lower = prev_q.lower().strip()
                                if self._are_questions_too_similar(question_lower, prev_q_lower):
                                    is_too_similar = True
                                    self.logger.warning(f"Question too similar to existing: '{result.question}' vs '{prev_q}'")
                                    break
                            
                            if not is_too_similar:
                                questions.append(
                                    QuizQuestion(
                                        type='Fill in the blank',
                                        question=result.question,
                                        correct_answer=result.answer
                                    )
                                )
                                generated_questions_text.append(result.question)
                                question_generated = True
                                self.logger.info(f"Generated unique question {i + 1}/{num_questions}")
                                break
                            else:
                                self.logger.warning(f"Semantically similar question detected, retrying... (attempt {attempt + 1})")
                        else:
                            self.logger.warning(f"Exact duplicate question detected, retrying... (attempt {attempt + 1})")
                
                except Exception as e:
                    self.logger.warning(f"Failed to generate question {i + 1}/{num_questions} on attempt {attempt + 1}: {str(e)}")
                    if attempt == max_attempts_per_question - 1:
                        self.logger.error(f"Could not generate unique question {i + 1} after {max_attempts_per_question} attempts")
            
            if not question_generated:
                self.logger.warning(f"Skipping question {i + 1} after exhausting all attempts")
        
        if not questions:
            raise CustomException(
                f"Failed to generate any questions for topic '{topic}' with difficulty '{difficulty}' "
                f"and question type '{question_type}' after multiple attempts."
            )

        return QuizResponse(questions=questions)
    
    def _are_questions_too_similar(self, q1: str, q2: str) -> bool:
        """Check if two questions are semantically too similar"""
        # Remove common question words
        common_words = {
            'what', 'is', 'are', 'the', 'a', 'an', 'in', 'of', 'to', 'for', 
            'and', 'or', 'which', 'how', 'can', 'does', 'do', 'when', 'where', 
            'why', 'who', 'with', 'from', 'by', 'at', 'as', 'on', 'be', 'this',
            'that', 'it', 'its', 'you', 'your', 'will', 'would', 'should', 'could'
        }
        
        def get_key_words(question: str) -> set:
            # Remove punctuation and split
            words = question.replace('?', '').replace('.', '').replace(',', '').replace('!', '').split()
            # Filter out common words and get key terms
            return {w.lower() for w in words if w.lower() not in common_words and len(w) > 2}
        
        words1 = get_key_words(q1)
        words2 = get_key_words(q2)
        
        if not words1 or not words2:
            return False
        
        # Calculate Jaccard similarity
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        if union == 0:
            return False
        
        similarity = intersection / union
        
        # If more than 70% of key words are the same, consider it too similar
        self.logger.debug(f"Similarity score: {similarity:.2f} between questions")
        return similarity > 0.7
