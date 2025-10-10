from langchain_groq import ChatGroq
from src.config.settings import settings
from typing import Optional

def get_groq_llm(temperature: Optional[float] = None):
    # Use provided temperature or default to setting
    # The default setting value is 0.9
    temp = temperature if temperature is not None else settings.TEMPERATURE
    return ChatGroq(
        api_key = settings.GROQ_API_KEY,
        model = settings.MODEL_NAME,
        temperature=temp,
        streaming=False
    )