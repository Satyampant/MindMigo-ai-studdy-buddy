from sqlalchemy.orm import Session
from src.database.models import Conversation, ChatMessageDB
from src.models.api_schemas import ChatMessage
from src.llm.groq_client import get_groq_llm
from src.prompts.templates import tutor_system_prompt
from typing import List
import uuid

class ChatService:
    def create_or_get_conversation(self, db: Session, student_id: str, conversation_id: str = None) -> str:
        if conversation_id:
            return conversation_id
        new_id = f"conv_{uuid.uuid4().hex[:12]}"
        db.add(Conversation(id=new_id, student_id=student_id))
        db.commit()
        return new_id

    def add_message_to_history(self, db: Session, conversation_id: str, role: str, content: str):
        db.add(ChatMessageDB(conversation_id=conversation_id, role=role, content=content))
        db.commit()

    def format_conversation_context(self, db: Session, conversation_id: str) -> List[ChatMessage]:
        messages = db.query(ChatMessageDB).filter(ChatMessageDB.conversation_id == conversation_id).order_by(ChatMessageDB.timestamp.desc()).limit(10).all()
        return [ChatMessage(role=msg.role, content=msg.content, timestamp=msg.timestamp) for msg in reversed(messages)]

    async def get_tutor_response(self, db: Session, conversation_id: str, student_message: str) -> str:
        context = self.format_conversation_context(db, conversation_id)
        history_text = "\n".join([f"{msg.role.capitalize()}: {msg.content}" for msg in context])
        prompt = f"{tutor_system_prompt}\n\nConversation History:\n{history_text}\n\nTutor:"
        llm = get_groq_llm(temperature=0.7)
        response = await llm.ainvoke(prompt)
        return response.content
