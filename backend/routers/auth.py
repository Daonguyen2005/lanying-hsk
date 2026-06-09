from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from database import get_db, User, Tutor, Booking, Course
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# ---- Pydantic Schemas ----
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "student"
    hsk_level: int = 5
    specialization: str = ""

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    name: str
    role: str

# ---- Helper Functions ---- (dùng bcrypt trực tiếp, không qua passlib)
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Khong the xac thuc thong tin",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

# ---- Routes ----
@router.post("/register", status_code=201)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email da ton tai!")
    if req.role == "tutor" and req.hsk_level < 5:
        raise HTTPException(status_code=400, detail="Gia sư phải có HSK từ cấp 5 trở lên!")

    user = User(
        name=req.name,
        email=req.email,
        password_hash=hash_password(req.password),
        role=req.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if req.role == "tutor":
        empty_tutor = Tutor(
            user_id=user.id,
            hsk_level=req.hsk_level,
            teaching_levels=str(req.hsk_level),
            hourly_rate=150000, # Đặt mặc định 150k/h
            specialization=req.specialization,
            bio="Xin chào, tôi là gia sư tiếng Trung. Rất vui được đồng hành cùng bạn trên con đường chinh phục HSK!",
            tags_vector="gia sư, tiếng trung, hsk",
            is_active=True # Kích hoạt ngay lập tức để hiện lên danh sách
        )
        db.add(empty_tutor)
        db.commit()

    return {"message": "Dang ky thanh cong!", "user_id": user.id}


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email hoac mat khau khong dung!")
    token = create_token({"sub": str(user.id), "role": user.role})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        name=user.name,
        role=user.role
    )

@router.get("/me/dashboard")
def get_user_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == "tutor":
        tutor = db.query(Tutor).filter(Tutor.user_id == current_user.id).first()
        if not tutor:
            raise HTTPException(status_code=404, detail="Tutor profile not found")
        
        # Lấy danh sách học sinh đã đặt lịch
        bookings = db.query(Booking).filter(Booking.tutor_id == tutor.id).all()
        booking_data = []
        for b in bookings:
            student = db.query(User).filter(User.id == b.student_id).first()
            booking_data.append({
                "id": b.id,
                "student_name": student.name if student else "Unknown",
                "status": b.status,
                "created_at": b.created_at
            })
            
        return {
            "role": "tutor",
            "name": current_user.name,
            "hsk_level": tutor.hsk_level,
            "teaching_levels": tutor.teaching_levels,
            "bookings": booking_data
        }
    else:
        # role == student
        bookings = db.query(Booking).filter(Booking.student_id == current_user.id).all()
        booking_data = []
        for b in bookings:
            tutor = db.query(Tutor).filter(Tutor.id == b.tutor_id).first()
            tutor_user = db.query(User).filter(User.id == tutor.user_id).first() if tutor else None
            booking_data.append({
                "id": b.id,
                "tutor_name": tutor_user.name if tutor_user else "Unknown Tutor",
                "status": b.status,
                "created_at": b.created_at
            })
            
        return {
            "role": "student",
            "name": current_user.name,
            "bookings": booking_data
        }
