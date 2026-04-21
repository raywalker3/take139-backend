"""Database models and setup for Take 139."""
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Use persistent volume path on Railway, fallback to local for dev
DB_PATH = os.environ.get("DATABASE_PATH", "./take139.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Submission(Base):
    """A completed assessment submission."""
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    pair_code = Column(String(32), unique=True, index=True, nullable=False)

    # Identity
    name = Column(String(200), nullable=True)
    email = Column(String(200), nullable=True, index=True)

    # Access context — which code was used? tracks to counselor later
    access_code_used = Column(String(100), nullable=True, index=True)

    # Intake answers (JSON stored as text)
    intake_json = Column(Text, nullable=True)

    # All answers (JSON stored as text)
    answers_json = Column(Text, nullable=False)

    # Computed results
    results_json = Column(Text, nullable=False)

    # The primary profile identifiers for quick filtering
    primary_trigger = Column(String(50), nullable=True, index=True)
    primary_core_question = Column(String(100), nullable=True, index=True)
    primary_mechanism = Column(String(50), nullable=True, index=True)
    primary_breakdown = Column(String(50), nullable=True, index=True)

    # Couple linking — once paired to a partner
    paired_with_code = Column(String(32), nullable=True, index=True)
    paired_at = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    emailed_to_user = Column(Boolean, default=False)
    emailed_to_admin = Column(Boolean, default=False)


def init_db():
    """Create tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
