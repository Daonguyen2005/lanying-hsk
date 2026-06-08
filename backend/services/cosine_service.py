import math
import json

# Vector kích thước 15 chiều:
# [
#   # Goals (0-3)
#   goal_hsk, goal_comm, goal_biz, goal_kids,
#   # Skills (4-7)
#   skill_listening_speaking, skill_pronunciation, skill_reading_writing, skill_grammar,
#   # Level (8-10)
#   level_beginner, level_intermediate, level_advanced,
#   # Age/Audience (11-12)
#   audience_kids, audience_adults,
#   # Mode (13-14)
#   mode_online, mode_offline
# ]

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
    
    return ", ".join(list(set(tags)))

def build_user_vector(current_level: str, goals: list, skills: list, modes: list, age: str) -> list:
    vector = [0] * 15

    # Goals
    if "hsk_exam" in goals: vector[0] = 1
    if "communication" in goals: vector[1] = 1
    if "business" in goals: vector[2] = 1
    if "kids" in goals: vector[3] = 1

    # Skills
    if "listening_speaking" in skills: vector[4] = 1
    if "pronunciation" in skills: vector[5] = 1
    if "reading_writing" in skills: vector[6] = 1
    if "grammar" in skills: vector[7] = 1

    # Level
    if current_level in ["beginner", "hsk1", "hsk2"]: vector[8] = 1
    if current_level in ["hsk3", "hsk4"]: vector[9] = 1
    if current_level in ["hsk5", "hsk6"]: vector[10] = 1

    # Age/Audience
    if age == "kids": vector[11] = 1
    if age in ["student", "adult"]: vector[12] = 1

    # Mode
    if "online" in modes: vector[13] = 1
    if "offline" in modes: vector[14] = 1

    return vector

def build_tutor_vector(tags_str: str) -> list:
    tags = tags_str.lower() if tags_str else ""
    return [
        # Goals
        1 if any(t in tags for t in ["hsk", "luyen thi", "giai de"]) else 0,
        1 if any(t in tags for t in ["giao tiep", "khau ngu", "phat am", "hoi thoai"]) else 0,
        1 if any(t in tags for t in ["thuong mai", "business", "dich thuat", "xuat nhap khau"]) else 0,
        1 if any(t in tags for t in ["tre em", "kids", "thieu nhi"]) else 0,
        
        # Skills
        1 if any(t in tags for t in ["nghe", "noi", "khau ngu", "giao tiep", "phan xa"]) else 0,
        1 if any(t in tags for t in ["phat am", "thanh dieu", "pinyin", "chuan"]) else 0,
        1 if any(t in tags for t in ["doc", "viet", "chu han", "viet lach"]) else 0,
        1 if any(t in tags for t in ["ngu phap", "cau truc", "chuyen sau"]) else 0,
        
        # Levels they teach
        1 if any(t in tags for t in ["co ban", "beginner", "hsk1", "hsk2"]) else 0,
        1 if any(t in tags for t in ["trung cap", "hsk3", "hsk4"]) else 0,
        1 if any(t in tags for t in ["nang cao", "hsk5", "hsk6", "chuyen sau", "phien dich"]) else 0,
        
        # Audience
        1 if any(t in tags for t in ["tre em", "thieu nhi"]) else 0,
        1 if any(t in tags for t in ["sinh vien", "nguoi di lam", "thuong mai", "dai hoc"]) else 1, # Default most can teach adults
        
        # Mode
        1, # Mặc định hỗ trợ Online
        1  # Mặc định hỗ trợ Offline
    ]

def cosine_similarity_pure(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = math.sqrt(sum(a * a for a in vec1))
    norm_b = math.sqrt(sum(b * b for b in vec2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

def recommend_tutors(user_vector: list, tutors: list, top_k: int = 3) -> list:
    if not tutors: return []
    scores = []
    for tutor in tutors:
        tutor_vec = build_tutor_vector(tutor.get("tags_vector", ""))
        score = cosine_similarity_pure(user_vector, tutor_vec)
        scores.append({**tutor, "similarity_score": round(float(score) * 100, 1)})
    
    scores.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scores[:top_k]
