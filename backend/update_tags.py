from database import SessionLocal, Tutor
import random

def update_tutor_tags():
    db = SessionLocal()
    try:
        print("Updating existing tutor tags to match 15D vector...")
        tutors = db.query(Tutor).all()
        
        # Enhanced tags matching new features
        enhanced_tags = [
            "giao tiep, thuong mai, hsk6, nghe, noi, phat am, nguoi di lam",
            "luyen thi, hsk5, cap toc, giai de, doc, viet, sinh vien, trung cap",
            "ban xu, phat am, hsk6, giao tiep, nghe, thanh dieu, nguoi di lam",
            "co ban, giao tiep, hsk4, nghe, noi, pinyin, sinh vien, trung cap",
            "khau ngu, nang cao, hsk6, phien dich, nghe, noi, phan xa, nguoi di lam",
            "thuong mai, hsk6, xuat nhap khau, nghe, doc, viet lach, nguoi di lam",
            "tre em, hsk3, co ban, phat am, nghe, noi, thieu nhi, kids",
            "dich thuat, hsk6, chuyen sau, doc, viet, ngu phap, nguoi di lam"
        ]
        
        for t in tutors:
            # Gán ngẫu nhiên tag mới phong phú hơn để test thuật toán
            t.tags_vector = random.choice(enhanced_tags)
            
        db.commit()
        print("Tags updated successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    update_tutor_tags()
