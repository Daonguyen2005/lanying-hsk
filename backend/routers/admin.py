from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, User, Tutor, Booking, Course
from routers.auth import get_current_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])

def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Khong co quyen truy cap admin")
    return current_user

@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    total_users = db.query(User).count()
    total_tutors = db.query(Tutor).count()
    total_students = db.query(User).filter(User.role == 'student').count()
    total_bookings = db.query(Booking).count()
    
    # Optional: fetch some recent bookings or users for the dashboard
    recent_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()
    
    recent_users_data = []
    for u in recent_users:
        recent_users_data.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "created_at": u.created_at
        })
        
    return {
        "total_users": total_users,
        "total_tutors": total_tutors,
        "total_students": total_students,
        "total_bookings": total_bookings,
        "recent_users": recent_users_data
    }
