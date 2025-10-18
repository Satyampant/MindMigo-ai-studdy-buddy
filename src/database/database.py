from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base

DATABASE_URL = "sqlite:///./studdy_buddy.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
