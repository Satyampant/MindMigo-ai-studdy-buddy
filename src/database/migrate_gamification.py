from src.database.database import engine
from src.database.models import Base

def run_migration():
    """Create gamification tables in the database"""
    Base.metadata.create_all(bind=engine)
    print("✅ Gamification tables created successfully!")
    print("   - student_gamification")
    print("   - student_badges")
    print("   - xp_transactions")

if __name__ == "__main__":
    run_migration()
