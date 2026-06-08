import random
import bcrypt
from database import SessionLocal, User, Tutor, Course, engine, Base

# Danh sách tên tiếng Việt ngẫu nhiên
HO = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý"]
TEN_DEM = ["Văn", "Thị", "Thanh", "Minh", "Thu", "Ngọc", "Hải", "Gia", "Đức", "Hoài", "Quang", "Hồng", "Tuấn", "Thùy", "Bảo"]
TEN = ["Anh", "Hà", "Linh", "Nam", "Long", "Trang", "Lan", "Hương", "Huy", "Khoa", "Hiếu", "Thảo", "Phương", "Nhung", "Cường", "Đạt", "Sơn", "Tâm", "Vy", "Yến"]

SPECIALIZATIONS = [
    "Giao tiếp thương mại", "Luyện thi HSK cấp tốc", "Phát âm chuẩn", 
    "Tiếng Trung giao tiếp", "Tiếng Trung trẻ em", "Dịch thuật chuyên sâu",
    "Tiếng Trung du lịch", "Ngữ pháp chuyên sâu", "Khẩu ngữ phản xạ"
]

def generate_random_name():
    return f"{random.choice(HO)} {random.choice(TEN_DEM)} {random.choice(TEN)}"

def generate_teaching_levels(hsk_level):
    # Giáo viên chỉ có thể dạy cấp độ nhỏ hơn hoặc bằng cấp độ HSK của bản thân
    # Trả về chuỗi ví dụ: "1,2,3"
    max_teach = hsk_level
    # Có giáo viên chỉ thích dạy sơ cấp dù họ HSK 6
    chosen_max = random.randint(min(3, max_teach), max_teach)
    levels = [str(i) for i in range(1, chosen_max + 1)]
    return ",".join(levels)

def generate_tags_vector(hsk_level, teaching_levels, specialization):
    tags = []
    
    # HSK Tags
    if "luyen thi" in specialization.lower(): tags.append("luyen thi, giai de")
    if "giao tiep" in specialization.lower() or "khau ngu" in specialization.lower(): tags.append("giao tiep, khau ngu, nghe, noi, phan xa")
    if "thuong mai" in specialization.lower(): tags.append("thuong mai, business, xuat nhap khau, nguoi di lam")
    if "tre em" in specialization.lower(): tags.append("tre em, kids, thieu nhi")
    if "phat am" in specialization.lower(): tags.append("phat am, thanh dieu, pinyin")
    if "dich thuat" in specialization.lower(): tags.append("doc, viet, dich thuat, viet lach")
    if "ngu phap" in specialization.lower(): tags.append("ngu phap, cau truc")
    
    # Levels Tags
    tags.append(f"hsk{hsk_level}")
    
    teach_arr = teaching_levels.split(",")
    for t in teach_arr:
        if t in ["1", "2"]: tags.append("co ban, beginner")
        if t in ["3", "4"]: tags.append("trung cap")
        if t in ["5", "6"]: tags.append("nang cao, chuyen sau")
    
    # Audience
    if "tre em" not in tags:
        tags.append(random.choice(["sinh vien, nguoi di lam", "nguoi di lam"]))
        
    return ", ".join(list(set(tags)))

def seed_data():
    db = SessionLocal()
    try:
        from database import SurveyResponse
        print("Đang xóa dữ liệu cũ (chỉ xóa User và Tutor)...")
        db.query(SurveyResponse).delete()
        db.query(Course).delete()
        db.query(Tutor).delete()
        
        # Xóa các User (trừ user admin/người dùng hiện tại, nhưng để đơn giản ta tạo lại)
        db.query(User).delete()
        db.commit()

        print("Đang tạo 20+ Gia sư mới...")
        password_hash = bcrypt.hashpw("123456".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        # Thêm 1 tài khoản Học viên test như cũ
        student_user = User(name="Nguyễn Văn Đạo", email="test@email.com", password_hash=password_hash, role="student")
        db.add(student_user)
        db.commit()

        # Tạo 25 Gia sư
        for i in range(25):
            name = generate_random_name()
            email = f"tutor{i+1}@email.com"
            user = User(name=name, email=email, password_hash=password_hash, role="tutor")
            db.add(user)
            db.commit()

            # Random HSK level (từ 4 đến 6, hiếm khi gia sư HSK dưới 4)
            hsk_level = random.choices([4, 5, 6], weights=[20, 40, 40])[0]
            teaching_levels = generate_teaching_levels(hsk_level)
            spec = random.choice(SPECIALIZATIONS)
            bio = f"Xin chào, tôi là {name}. Tôi đã đạt chứng chỉ HSK {hsk_level} và có nhiều năm kinh nghiệm giảng dạy tiếng Trung. Thế mạnh của tôi là {spec}."
            
            tags = generate_tags_vector(hsk_level, teaching_levels, spec)
            
            tutor = Tutor(
                user_id=user.id,
                bio=bio,
                hsk_level=hsk_level,
                teaching_levels=teaching_levels,
                specialization=spec,
                hourly_rate=random.choice([100000, 150000, 200000, 250000, 300000]),
                is_active=True,
                tags_vector=tags
            )
            db.add(tutor)
        
        db.commit()
        print("Đã tạo xong 25 gia sư chuẩn logic (Chỉ dạy cấp <= HSK của mình)!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
