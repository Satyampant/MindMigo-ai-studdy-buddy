from langchain.output_parsers import PydanticOutputParser
from src.models.question_schemas import MCQQuestion,FillBlankQuestion
from src.prompts.templates import (
    mcq_prompt_template, mcq_prompt_with_context_template,
    fill_blank_prompt_template, fill_blank_prompt_with_context_template
)
from src.llm.groq_client import get_groq_llm
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException
import random
from typing import List, Optional

# Note: All methods using the LLM are now asynchronous.

class QuestionGenerator:
    def __init__(self):
        # Base LLM - we'll create variations with different temperatures
        self.logger = get_logger(self.__class__.__name__)

    def _get_llm_with_variation(self):
        """Get LLM with slightly varied temperature for diversity"""
        base_temp = settings.TEMPERATURE
        # Add small random variation to temperature (±0.1)
        varied_temp = base_temp + random.uniform(-0.1, 0.1)
        # Clamp between 0.7 and 1.0
        varied_temp = max(0.7, min(1.0, varied_temp))
        return get_groq_llm(temperature=varied_temp)

    async def _retry_and_parse(self, prompt, parser, topic, difficulty, previous_questions: Optional[List[str]] = None):
        """
        Retries the LLM call and attempts to parse the output asynchronously.
        """
        for attempt in range(settings.MAX_RETRIES): # The number of max retries is 3
            try:
                self.logger.info(f"Generating question for topic {topic} with difficulty {difficulty}, attempt {attempt + 1}")

                # Get LLM with varied temperature for diversity
                llm = self._get_llm_with_variation()
                
                # Format prompt with or without context
                if previous_questions:
                    formatted_prompt = prompt.format(
                        topic=topic,
                        difficulty=difficulty,
                        previous_questions="\n".join([f"- {q}" for q in previous_questions])
                    )
                else:
                    formatted_prompt = prompt.format(topic=topic, difficulty=difficulty)
                
                # Switched to the asynchronous invoke method (ainvoke)
                response = await llm.ainvoke(formatted_prompt)

                parsed = parser.parse(response.content)

                self.logger.info("Sucesfully parsed the question")

                return parsed

            except Exception as e:
                self.logger.error(f"Error-Failed to parse/generate question: {str(e)} on attempt {attempt + 1}")
                if attempt == settings.MAX_RETRIES - 1:
                    # Raise CustomException if maximum retries reached
                    raise CustomException(f"Failed to generate question after {settings.MAX_RETRIES} attempts", e)

    # Made this method asynchronous
    async def generate_mcq(self, topic: str, difficulty: str = 'medium', previous_questions: Optional[List[str]] = None) -> MCQQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=MCQQuestion)

            # Use context-aware prompt if previous questions exist
            if previous_questions and len(previous_questions) > 0:
                prompt = mcq_prompt_with_context_template
            else:
                prompt = mcq_prompt_template

            # Await the async retry function
            question = await self._retry_and_parse(prompt, parser, topic, difficulty, previous_questions)

            # Normalize for comparison
            normalized_options = [opt.strip() for opt in question.options]
            normalized_answer = question.correct_answer.strip()

            if len(question.options) != 4:
                raise ValueError(f"MCQ must have exactly 4 options, got {len(question.options)}")

            if normalized_answer not in normalized_options:
                raise ValueError(f"Correct answer '{question.correct_answer}' not found in options: {question.options}")

            self.logger.info("Generated a valid MCQ Question")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate MCQ : {str(e)}")
            if isinstance(e, CustomException):
                raise
            raise CustomException("MCQ generation failed" , e)

    # Made this method asynchronous
    async def generate_fill_blank(self, topic: str, difficulty: str = 'medium', previous_questions: Optional[List[str]] = None) -> FillBlankQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=FillBlankQuestion)

            # Use context-aware prompt if previous questions exist
            if previous_questions and len(previous_questions) > 0:
                prompt = fill_blank_prompt_with_context_template
            else:
                prompt = fill_blank_prompt_template

            # Await the async retry function
            question = await self._retry_and_parse(prompt, parser, topic, difficulty, previous_questions)

            if "___" not in question.question:
                raise ValueError("Fill in blanks should contain '___'")

            self.logger.info("Generated a valid Fill in Blanks Question")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate fillups : {str(e)}")
            if isinstance(e, CustomException):
                raise
            raise CustomException("Fill in blanks generation failed" , e)