from langchain_groq import ChatGroq
from src.config.settings import settings

def get_groq_llm() -> ChatGroq:
    return ChatGroq(
        model=settings.GROQ_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=0.7,
        max_retries=3,
        timeout=30
    )