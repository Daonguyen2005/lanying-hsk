from database import Base, engine, SessionLocal, User, Tutor, Course
from routers.auth import hash_password

def reset_db():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables (with Unicode/NVARCHAR)...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("Seeding data...")
        # Add a test user
        user = User(
            name="Nguyễn Văn Đạo",
            email="test@email.com",
            password_hash=hash_password("123456"),
            role="student"
        )
        db.add(user)
        
        # Add some mock tutors
        tutor_user1 = User(name="Lê Thị Hằng", email="hang@tutor.com", password_hash=hash_password("123"), role="tutor")
        tutor_user2 = User(name="Trần Văn Nam", email="nam@tutor.com", password_hash=hash_password("123"), role="tutor")
        tutor_user3 = User(name="Vương Ngữ Yên", email="yen@tutor.com", password_hash=hash_password("123"), role="tutor")
        
        db.add_all([tutor_user1, tutor_user2, tutor_user3])
        db.commit()
        
        t1 = Tutor(user_id=tutor_user1.id, hsk_level=6, hourly_rate=200000, specialization="Giao tiếp thương mại", bio="Giảng viên đại học Ngoại Ngữ, kinh nghiệm 5 năm", tags_vector="giao tiep, thuong mai, hsk6")
        t2 = Tutor(user_id=tutor_user2.id, hsk_level=5, hourly_rate=150000, specialization="Luyện thi HSK", bio="Từng du học Bắc Kinh, chuyên luyện HSK cấp tốc", tags_vector="luyen thi, hsk5, cap toc")
        t3 = Tutor(user_id=tutor_user3.id, hsk_level=6, hourly_rate=250000, specialization="Phát âm chuẩn", bio="Người bản xứ Đài Loan, dạy phát âm chuẩn", tags_vector="ban xu, phat am, hsk6")
        
        db.add_all([t1, t2, t3])
        db.commit()
        print("Database reset & seeded successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    reset_db()
