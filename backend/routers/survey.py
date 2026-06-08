from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db, Tutor, User, SurveyResponse
from services.cosine_service import build_user_vector, recommend_tutors
import json

router = APIRouter(prefix="/api/survey", tags=["Survey & Recommendation"])

class SurveyRequest(BaseModel):
    current_level: str
    goals: List[str]
    skills: List[str]
    modes: List[str]
    age: str
    user_id: Optional[int] = None

@router.post("/")
def submit_survey(req: SurveyRequest, db: Session = Depends(get_db)):
    # Lưu kết quả khảo sát
    if req.user_id:
        survey = SurveyResponse(
            user_id=req.user_id,
            current_level=req.current_level,
            goals=json.dumps(req.goals),
            skills=json.dumps(req.skills),
            modes=json.dumps(req.modes),
            age=req.age
        )
        db.add(survey)
        db.commit()

    # Lấy danh sách gia sư từ DB
    tutor_records = db.query(Tutor, User.name).join(User).filter(Tutor.is_active == True).all()
    tutors_data = []
    for tutor, name in tutor_records:
        tutors_data.append({
            "id": tutor.id,
            "name": name,
            "tags_vector": tutor.tags_vector or "{}",
            "hourly_rate": tutor.hourly_rate,
            "hsk_level": tutor.hsk_level,
            "teaching_levels": tutor.teaching_levels,
            "specialization": tutor.specialization,
            "bio": tutor.bio,
        })

    # Tính Cosine Similarity
    user_vec = build_user_vector(req.current_level, req.goals, req.skills, req.modes, req.age)
    recommendations = recommend_tutors(user_vec, tutors_data, top_k=3)

    return {
        "user_vector": user_vec,
        "recommendations": recommendations
    }
