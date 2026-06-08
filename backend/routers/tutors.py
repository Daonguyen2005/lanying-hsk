from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, Tutor, User, Booking
from routers.auth import get_current_user
from typing import List, Optional
import json
from datetime import datetime
from services.cosine_service import generate_tags_vector

router = APIRouter(prefix="/api/tutors", tags=["Tutors"])

class TutorResponse(BaseModel):
    id: int
    name: str
    bio: Optional[str]
    hsk_level: Optional[int]
    teaching_levels: Optional[str]
    hourly_rate: Optional[float]
    specialization: Optional[str]

    class Config:
        from_attributes = True

class TutorUpdateRequest(BaseModel):
    hsk_level: int
    teaching_levels: str
    hourly_rate: float
    specialization: str
    bio: str

@router.get("/me")
def get_my_tutor_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "tutor":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Khong phai gia su")
    
    tutor = db.query(Tutor).filter(Tutor.user_id == current_user.id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="Ho so khong ton tai")
    
    return {
        "id": tutor.id,
        "name": current_user.name,
        "bio": tutor.bio,
        "hsk_level": tutor.hsk_level,
        "teaching_levels": tutor.teaching_levels,
        "hourly_rate": tutor.hourly_rate,
        "specialization": tutor.specialization,
        "is_active": tutor.is_active
    }

@router.put("/me")
def update_my_tutor_profile(req: TutorUpdateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "tutor":
        raise HTTPException(status_code=403, detail="Khong phai gia su")
    
    if req.hsk_level < 5:
        raise HTTPException(status_code=400, detail="Gia sư phải có HSK từ cấp 5 trở lên!")

    tutor = db.query(Tutor).filter(Tutor.user_id == current_user.id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="Ho so khong ton tai")
    
    # Kiem tra logic hsk
    max_teach = req.hsk_level
    teach_arr = req.teaching_levels.split(',')
    for t in teach_arr:
        if t and int(t.strip()) > max_teach:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail=f"Khong the day cap do cao hon HSK ban than ({req.hsk_level})")
            
    tutor.hsk_level = req.hsk_level
    tutor.teaching_levels = req.teaching_levels
    tutor.hourly_rate = req.hourly_rate
    tutor.specialization = req.specialization
    tutor.bio = req.bio
    tutor.is_active = True # Da cap nhat du lieu thi cho active
    
    # Cap nhat vector the tags
    tutor.tags_vector = generate_tags_vector(req.hsk_level, req.teaching_levels, req.specialization)
    
    db.commit()
    return {"message": "Cap nhat ho so thanh cong"}

@router.get("/", response_model=List[TutorResponse])
def get_tutors(hsk_level: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Tutor, User.name).join(User, Tutor.user_id == User.id).filter(Tutor.is_active == True)
    if hsk_level:
        query = query.filter(Tutor.hsk_level >= hsk_level)
    results = query.all()
    tutors = []
    for tutor, name in results:
        tutors.append(TutorResponse(
            id=tutor.id,
            name=name,
            bio=tutor.bio,
            hsk_level=tutor.hsk_level,
            teaching_levels=tutor.teaching_levels,
            hourly_rate=tutor.hourly_rate,
            specialization=tutor.specialization
        ))
    return tutors

@router.get("/{tutor_id}")
def get_tutor_detail(tutor_id: int, db: Session = Depends(get_db)):
    tutor = db.query(Tutor).filter(Tutor.id == tutor_id).first()
    if not tutor:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy gia sư")
    user = db.query(User).filter(User.id == tutor.user_id).first()
    return {
        "id": tutor.id,
        "name": user.name,
        "bio": tutor.bio,
        "hsk_level": tutor.hsk_level,
        "teaching_levels": tutor.teaching_levels,
        "hourly_rate": tutor.hourly_rate,
        "specialization": tutor.specialization,
        "courses": [{"id": c.id, "name": c.name, "price": c.price} for c in tutor.courses]
    }

class BookingRequest(BaseModel):
    note: str = ""

@router.post("/{tutor_id}/book")
def book_tutor(tutor_id: int, req: BookingRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tutor = db.query(Tutor).filter(Tutor.id == tutor_id).first()
    if not tutor:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy gia sư")
    
    booking = Booking(
        student_id=current_user.id,
        tutor_id=tutor.id,
        scheduled_at=datetime.utcnow(),
        status="pending",
        note=req.note
    )
    db.add(booking)
    db.commit()
    return {"message": "Dat lich thanh cong"}

class BookingStatusRequest(BaseModel):
    status: str

@router.put("/bookings/{booking_id}")
def update_booking_status(booking_id: int, req: BookingStatusRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "tutor":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Chỉ gia sư mới được duyệt lớp")
    
    tutor = db.query(Tutor).filter(Tutor.user_id == current_user.id).first()
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking or booking.tutor_id != tutor.id:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch học")
        
    booking.status = req.status
    db.commit()
    return {"message": "Cập nhật thành công", "status": req.status}
