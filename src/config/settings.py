import os
from dotenv import load_dotenv

load_dotenv()

class Settings():

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable is not set. Please set it in your .env file.")

    # Recommended models for AI tutor (in order of quality):
    # 1. "llama-3.3-70b-versatile" - Best quality, latest knowledge (Dec 2024)
    # 2. "llama-3.1-70b-versatile" - Good quality, balanced speed/accuracy
    # 3. "mixtral-8x7b-32768" - Good for longer context
    # 4. "llama-3.1-8b-instant" - Fastest but least accurate (current)
    
    MODEL_NAME = "llama-3.3-70b-versatile"  # Upgraded for better AI/ML knowledge
    
    TEMPERATURE = 0.9

    MAX_RETRIES = 3


settings = Settings()  