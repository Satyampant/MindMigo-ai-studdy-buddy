from langchain_core.prompts import PromptTemplate
from src.common.custom_exception import CustomException
from src.llm.groq_client import get_groq_llm
from src.common.logger import get_logger

logger = get_logger("ContentGenerator")

async def generate_content_for_topic(topic: str) -> str:
    """Generates comprehensive content for a given topic."""
    # Use a low temperature for factual content extraction
    LLM = get_groq_llm(temperature=0.1)

    prompt_template = PromptTemplate.from_template(
        "Generate a comprehensive and detailed technical summary of the topic: '{topic}'. "
        "The summary should be approximately 300-500 words long and rich in facts, concepts, and relationships suitable for creating a knowledge graph. "
        "The final output must be ONLY the content, nothing else. Do not add any conversational phrases or introductions."
    )
    prompt = prompt_template.format(topic=topic)

    try:
        logger.info(f"Generating content for topic: {topic}")
        response = await LLM.ainvoke(prompt)
        return response.content
    except Exception as e:
        logger.error(f"Failed to generate content for topic '{topic}': {str(e)}")
        raise CustomException(f"Failed to generate content for topic '{topic}'", e)