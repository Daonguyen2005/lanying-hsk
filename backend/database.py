from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# =====================
# ORM Models
# =====================

class User(Base):
    __tablename__ = "users"
    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(Unicode(100), nullable=False)
    email         = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role          = Column(String(20), default="student")
    created_at    = Column(DateTime, default=datetime.utcnow)

    tutor_profile = relationship("Tutor", back_populates="user", uselist=False)
    bookings      = relationship("Booking", foreign_keys="Booking.student_id", back_populates="student")

class Tutor(Base):
    __tablename__ = "tutors"
    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"), nullable=False)
    bio             = Column(Unicode(1000))
    hsk_level       = Column(Integer)  # Bằng cấp cao nhất của gia sư
    teaching_levels = Column(Unicode(100)) # Các cấp độ có thể dạy, vd: "1,2,3"
    hourly_rate     = Column(Float)
    specialization  = Column(Unicode(255))
    tags_vector     = Column(String(500))
    is_active       = Column(Boolean, default=True)
    created_at      = Column(DateTime, default=datetime.utcnow)

    user     = relationship("User", back_populates="tutor_profile")
    courses  = relationship("Course", back_populates="tutor")
    bookings = relationship("Booking", back_populates="tutor")

class Course(Base):
    __tablename__ = "courses"
    id             = Column(Integer, primary_key=True, index=True)
    tutor_id       = Column(Integer, ForeignKey("tutors.id"))
    name           = Column(Unicode(200), nullable=False)
    hsk_level      = Column(Integer)
    description    = Column(Unicode(2000))
    price          = Column(Float)
    duration_weeks = Column(Integer)
    is_active      = Column(Boolean, default=True)
    created_at     = Column(DateTime, default=datetime.utcnow)

    tutor = relationship("Tutor", back_populates="courses")

class Booking(Base):
    __tablename__ = "bookings"
    id             = Column(Integer, primary_key=True, index=True)
    student_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    tutor_id       = Column(Integer, ForeignKey("tutors.id"), nullable=False)
    course_id      = Column(Integer, ForeignKey("courses.id"))
    scheduled_at   = Column(DateTime, nullable=False)
    duration_hours = Column(Integer, default=1)
    status         = Column(String(20), default="pending")
    note           = Column(Unicode(500))
    created_at     = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", foreign_keys=[student_id], back_populates="bookings")
    tutor   = relationship("Tutor", back_populates="bookings")

class SurveyResponse(Base):
    __tablename__ = "survey_responses"
    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, ForeignKey("users.id"))
    current_level  = Column(String(50))
    goals          = Column(Unicode(500))
    skills         = Column(Unicode(500))
    modes          = Column(Unicode(200))
    age            = Column(String(50))
    created_at     = Column(DateTime, default=datetime.utcnow)


# Dependency cho FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
