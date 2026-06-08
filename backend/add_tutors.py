from database import SessionLocal, User, Tutor
from routers.auth import hash_password

def add_more_tutors():
    db = SessionLocal()
    try:
        print("Adding more tutors...")
        
        # Tạo thêm 6 gia sư mới
        tutors_data = [
            {"name": "Trần Thanh Tâm", "email": "tam@tutor.com", "hsk": 4, "rate": 100000, "spec": "Tiếng Trung giao tiếp cơ bản", "bio": "Giọng chuẩn phổ thông, chuyên dạy cho người mới bắt đầu", "tags": "co ban, giao tiep, hsk4"},
            {"name": "Lưu Học Nghĩa", "email": "nghia@tutor.com", "hsk": 6, "rate": 300000, "spec": "Khẩu ngữ nâng cao", "bio": "Từng làm phiên dịch viên cấp cao tại Bắc Kinh, chuyên luyện phản xạ", "tags": "khau ngu, nang cao, hsk6, phien dich"},
            {"name": "Ngô Cẩn Ngôn", "email": "ngon@tutor.com", "hsk": 5, "rate": 180000, "spec": "Luyện thi HSK 5", "bio": "Bí kíp giải đề HSK 5 bao đậu, giáo trình tự biên soạn", "tags": "luyen thi, hsk5, giai de"},
            {"name": "Đinh Vũ Hề", "email": "he@tutor.com", "hsk": 6, "rate": 220000, "spec": "Tiếng Trung thương mại", "bio": "Có kinh nghiệm startup tại Quảng Châu, chuyên tiếng Trung xuất nhập khẩu", "tags": "thuong mai, hsk6, xuat nhap khau"},
            {"name": "Dương Tử", "email": "tu@tutor.com", "hsk": 3, "rate": 80000, "spec": "Tiếng Trung trẻ em", "bio": "Dạy bằng phương pháp trò chơi, bài hát, giúp bé tiếp thu tự nhiên", "tags": "tre em, hsk3, co ban"},
            {"name": "Bạch Kính Đình", "email": "tinh@tutor.com", "hsk": 6, "rate": 280000, "spec": "Luyện dịch thuật", "bio": "Chuyên gia dịch thuật cabin, luyện dịch viết và nói chuyên sâu", "tags": "dich thuat, hsk6, chuyen sau"}
        ]
        
        users_to_add = []
        tutors_to_add = []
        
        for data in tutors_data:
            # Check if email exists
            existing_user = db.query(User).filter(User.email == data["email"]).first()
            if not existing_user:
                u = User(name=data["name"], email=data["email"], password_hash=hash_password("123"), role="tutor")
                db.add(u)
                db.commit() # commit to get user id
                db.refresh(u)
                
                t = Tutor(user_id=u.id, hsk_level=data["hsk"], hourly_rate=data["rate"], specialization=data["spec"], bio=data["bio"], tags_vector=data["tags"])
                db.add(t)
                db.commit()
                
        print("Successfully added 6 more tutors!")
    finally:
        db.close()

if __name__ == "__main__":
    add_more_tutors()
