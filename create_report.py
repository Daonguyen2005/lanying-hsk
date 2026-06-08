"""
create_report.py - Tao bao cao Word hoan chinh cho du an Lanying HSK
"""
import os
import shutil
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import docx

BASE = Path(__file__).parent
ARTIFACT_DIR = Path(r"C:\Users\VanDao\.gemini\antigravity\brain\7d0e1048-a0e2-410c-92be-748353d78493")
ER_IMG    = ARTIFACT_DIR / "er_diagram_1780845661689.png"
ARCH_IMG  = ARTIFACT_DIR / "system_architecture_1780845682683.png"
UC_AUTH   = ARTIFACT_DIR / "usecase_auth_1780846499397.png"
UC_STUDENT= ARTIFACT_DIR / "usecase_student_1780846520788.png"
UC_TUTOR  = ARTIFACT_DIR / "usecase_tutor_1780846544184.png"
UC_BOOKING= ARTIFACT_DIR / "usecase_booking_1780846566921.png"

FONT_NAME = "Times New Roman"
DEFAULT_SIZE = 12

def set_doc_font(doc):
    """Dat phong chu mac dinh Times New Roman 12 cho toan bo tai lieu."""
    from docx.oxml.ns import qn
    # Normal style
    style = doc.styles["Normal"]
    font = style.font
    font.name = FONT_NAME
    font.size = Pt(DEFAULT_SIZE)
    # Also set East Asian font
    rPr = style.element.get_or_add_rPr()
    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), FONT_NAME)
    rFonts.set(qn("w:hAnsi"), FONT_NAME)
    rFonts.set(qn("w:cs"), FONT_NAME)
    rPr.insert(0, rFonts)
    # Update heading styles
    for i in range(1, 5):
        hstyle = doc.styles["Heading " + str(i)]
        hstyle.font.name = FONT_NAME
        hrPr = hstyle.element.get_or_add_rPr()
        hrFonts = OxmlElement("w:rFonts")
        hrFonts.set(qn("w:ascii"), FONT_NAME)
        hrFonts.set(qn("w:hAnsi"), FONT_NAME)
        hrFonts.set(qn("w:cs"), FONT_NAME)
        hrPr.insert(0, hrFonts)

def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def add_heading(doc, text, level=1, color_hex=None):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = FONT_NAME
        if level == 1:
            run.font.size = Pt(14)
        elif level == 2:
            run.font.size = Pt(13)
        else:
            run.font.size = Pt(DEFAULT_SIZE)
        if color_hex:
            run.font.color.rgb = RGBColor.from_string(color_hex)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(6)
    return h

def add_para(doc, text, bold=False, size=None, color=None):
    if size is None:
        size = DEFAULT_SIZE
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = Pt(20)  # 1.5 line spacing
    return p

def add_image_safe(doc, img_path, caption=None, width=5.5):
    if Path(img_path).exists():
        doc.add_picture(str(img_path), width=Inches(width))
        last = doc.paragraphs[-1]
        last.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if caption:
            cap = doc.add_paragraph(caption)
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap.runs[0].font.name = FONT_NAME
            cap.runs[0].font.size = Pt(11)
            cap.runs[0].italic = True
    else:
        doc.add_paragraph(u"[Hinh anh khong tim thay: " + str(img_path) + u"]")

def add_table_with_header(doc, headers, rows, header_bg="2F5496"):
    table = doc.add_table(rows=1+len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header row
    hdr = table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.text = h
        set_cell_bg(cell, header_bg)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.runs[0]
        run.bold = True
        run.font.name = FONT_NAME
        run.font.color.rgb = RGBColor(255, 255, 255)
        run.font.size = Pt(DEFAULT_SIZE)
    # Data rows
    for ri, row_data in enumerate(rows):
        row = table.rows[ri+1]
        for ci, val in enumerate(row_data):
            cell = row.cells[ci]
            cell.text = str(val)
            run = cell.paragraphs[0].runs[0]
            run.font.name = FONT_NAME
            run.font.size = Pt(DEFAULT_SIZE)
            if ri % 2 == 0:
                set_cell_bg(cell, "DCE6F1")
    return table


def main():
    doc = Document()
    set_doc_font(doc)  # Times New Roman 12 toan bo tai lieu

    # ========== CAI DAT MARGIN ==========

    from docx.oxml.ns import qn
    section = doc.sections[0]
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(3)
    section.right_margin = Cm(2)

    # ========== TRANG BÌA ==========
    doc.add_paragraph()
    doc.add_paragraph()
    cover_school = doc.add_paragraph(u"TR\u01af\u1edcNG \u0110\u1ea0I H\u1eccC KINH T\u1ebe K\u1ef8 THU\u1eacT B\u00ccNH D\u01af\u01a0NG")
    cover_school.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_school.runs[0].font.name = FONT_NAME
    cover_school.runs[0].bold = True
    cover_school.runs[0].font.size = Pt(14)

    cover_dept = doc.add_paragraph(u"KHOA C\u00d4NG NGH\u1ec6 TH\u00d4NG TIN")
    cover_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_dept.runs[0].font.name = FONT_NAME
    cover_dept.runs[0].font.size = Pt(13)

    doc.add_paragraph()
    doc.add_paragraph()

    cover_title = doc.add_paragraph(u"B\u00c1O C\u00c1O \u0110\u1ed2 \u00c1N M\u00d4N H\u1eccC")
    cover_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_title.runs[0].font.name = FONT_NAME
    cover_title.runs[0].bold = True
    cover_title.runs[0].font.size = Pt(20)
    cover_title.runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    doc.add_paragraph()

    cover_proj = doc.add_paragraph(u"WEBSITE N\u1ec0N T\u1ea2NG GIA S\u01af TI\u1eacNG TRUNG TR\u1ef0C TUY\u1eacN")
    cover_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_proj.runs[0].font.name = FONT_NAME
    cover_proj.runs[0].bold = True
    cover_proj.runs[0].font.size = Pt(16)
    cover_proj.runs[0].font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    cover_sub = doc.add_paragraph("Lanying HSK Platform")
    cover_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_sub.runs[0].font.name = FONT_NAME
    cover_sub.runs[0].italic = True
    cover_sub.runs[0].font.size = Pt(13)

    doc.add_paragraph()
    doc.add_paragraph()

    for line in [
        (u"Sinh vi\u00ean th\u1ef1c hi\u1ec7n:", True),
        (u"1. Nguy\u1ec5n V\u0103n \u0110\u1ea1o", False),
        (u"2. \u0110o\u00e0n Nguy\u1ec5n Tr\u01b0\u1eddng Uy", False),
        ("", False),
        (u"Gi\u1ea3ng vi\u00ean h\u01b0\u1edbng d\u1eabn:", True),
        (u"Nguy\u1ec5n H\u1ed3 H\u1ea3i", False),
        ("", False),
        (u"H\u1ecdc k\u1ef3 II \u2013 N\u0103m h\u1ecdc 2024\u20132025", False),
    ]:
        p = doc.add_paragraph(line[0])
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p.runs:
            p.runs[0].font.name = FONT_NAME
            p.runs[0].bold = line[1]
            p.runs[0].font.size = Pt(DEFAULT_SIZE)

    doc.add_page_break()

    # ========== MUC LUC ==========
    add_heading(doc, u"M\u1ee4C L\u1ee4C", level=1, color_hex="1F497D")
    toc_items = [
        ("I.",    u"Gi\u1edbi thi\u1ec7u \u0111\u1ec1 t\u00e0i", 3),
        ("II.",   u"Ph\u00e2n t\u00edch y\u00eau c\u1ea7u", 3),
        ("III.",  u"Thi\u1ebft k\u1ebf h\u1ec7 th\u1ed1ng", 4),
        ("  3.1", u"S\u01a1 \u0111\u1ed3 ki\u1ebfn tr\u00fac h\u1ec7 th\u1ed1ng", 4),
        ("  3.2", u"S\u01a1 \u0111\u1ed3 c\u01a1 s\u1edf d\u1eef li\u1ec7u (ER)", 5),
        ("  3.3", u"S\u01a1 \u0111\u1ed3 Use Case", 5),
        ("  3.4", u"Ph\u00e2n quy\u1ec1n ng\u01b0\u1eddi d\u00f9ng", 7),
        ("IV.",   u"C\u00f4ng ngh\u1ec7 s\u1eed d\u1ee5ng", 8),
        ("V.",    u"C\u00e0i \u0111\u1eb7t v\u00e0 tri\u1ec3n khai", 9),
        ("VI.",   u"M\u00f4 t\u1ea3 ch\u1ee9c n\u0103ng chi ti\u1ebft", 10),
        ("  6.1", u"Module \u0110\u0103ng nh\u1eadp / \u0110\u0103ng k\u00fd", 10),
        ("  6.2", u"Module H\u1ecdc sinh", 11),
        ("  6.3", u"Module Gi\u00e1o vi\u00ean", 11),
        ("  6.4", u"Module Kh\u1ea3o s\u00e1t l\u1ed9 tr\u00ecnh h\u1ecdc", 12),
        ("  6.5", u"Module \u0110\u1eb7t l\u1ecbch gia s\u01b0", 12),
        ("VII.",  "API Backend", 13),
        ("VIII.", u"K\u1ebft qu\u1ea3 \u0111\u1ea1t \u0111\u01b0\u1ee3c", 15),
        ("IX.",   u"K\u1ebft lu\u1eadn v\u00e0 h\u01b0\u1edbng ph\u00e1t tri\u1ec3n", 16),
    ]
    for num, title, page in toc_items:
        p = doc.add_paragraph()
        run1 = p.add_run(num + "  " + title)
        run1.font.name = FONT_NAME
        run1.font.size = Pt(DEFAULT_SIZE)
        run2 = p.add_run("\t" + str(page))
        run2.font.name = FONT_NAME
        run2.font.size = Pt(DEFAULT_SIZE)
        p.paragraph_format.space_after = Pt(2)

    doc.add_page_break()

    # ========== CHUONG I: GIOI THIEU ==========
    add_heading(doc, "I. GIỚI THIỆU ĐỀ TÀI", level=1, color_hex="1F497D")

    add_heading(doc, "1.1. Bối cảnh và lý do chọn đề tài", level=2)
    add_para(doc, "Trong bối cảnh hội nhập kinh tế quốc tế ngày càng sâu rộng, đặc biệt là sự phát triển mạnh mẽ của quan hệ kinh tế - thương mại Việt Nam – Trung Quốc, nhu cầu học tiếng Trung trong cộng đồng ngày càng tăng cao. Theo khảo sát thực tế, số lượng người học tiếng Trung tại Việt Nam tăng trưởng mỗi năm, đặc biệt trong độ tuổi 18–35.")
    add_para(doc, "Tuy nhiên, thị trường gia sư tiếng Trung hiện tại còn nhiều hạn chế: thiếu nền tảng kết nối chuyên biệt, khó đánh giá chất lượng gia sư, không có cơ chế xác minh trình độ chuẩn mực. Đề tài \"Nền tảng Gia sư Tiếng Trung Trực tuyến – Lanying HSK\" ra đời nhằm giải quyết những bất cập trên.")

    add_heading(doc, "1.2. Mục tiêu đề tài", level=2)
    goals = [
        "Xây dựng nền tảng web kết nối học sinh với gia sư tiếng Trung có chứng chỉ HSK.",
        "Đảm bảo chất lượng dạy học: chỉ gia sư đạt HSK 5 trở lên mới được đăng ký giảng dạy.",
        "Phân quyền rõ ràng giữa Học sinh và Giáo viên với giao diện riêng biệt.",
        "Tích hợp AI (Google Gemini) để gợi ý lộ trình học cá nhân hóa.",
        "Cung cấp hệ thống đặt lịch và quản lý lớp học trực tuyến.",
    ]
    for g in goals:
        p = doc.add_paragraph(g, style="List Bullet")
        p.runs[0].font.size = Pt(11)

    add_heading(doc, "1.3. Phạm vi đề tài", level=2)
    add_para(doc, "Phạm vi thực hiện trong khuôn khổ đồ án: xây dựng giao diện web responsive, backend RESTful API với FastAPI, cơ sở dữ liệu SQLite, và tích hợp Gemini AI chatbot. Không bao gồm thanh toán trực tuyến và ứng dụng di động.")

    doc.add_page_break()

    # ========== CHƯƠNG II: PHÂN TÍCH YÊU CẦU ==========
    add_heading(doc, "II. PHÂN TÍCH YÊU CẦU", level=1, color_hex="1F497D")

    add_heading(doc, "2.1. Yêu cầu chức năng", level=2)
    func_reqs = [
        ("REQ-01", "Đăng ký tài khoản Học sinh", "Người dùng có thể tạo tài khoản học sinh với email và mật khẩu.", "Cao"),
        ("REQ-02", "Đăng ký tài khoản Giáo viên", "Người dùng đăng ký làm gia sư, bắt buộc phải có HSK ≥ 5.", "Cao"),
        ("REQ-03", "Đăng nhập phân quyền", "Hệ thống phân biệt đăng nhập Học sinh / Giáo viên, redirect đúng trang.", "Cao"),
        ("REQ-04", "Trang chủ Học sinh", "Hiển thị danh sách gia sư, chatbot AI, khảo sát lộ trình học.", "Cao"),
        ("REQ-05", "Trang chủ Giáo viên", "Dashboard riêng cho giáo viên: xem đặt lịch, duyệt/từ chối học sinh.", "Cao"),
        ("REQ-06", "Khảo sát lộ trình học", "Học sinh hoàn thành khảo sát để AI gợi ý lộ trình phù hợp.", "Trung bình"),
        ("REQ-07", "Đặt lịch gia sư", "Học sinh chọn gia sư và gửi yêu cầu đặt lịch.", "Cao"),
        ("REQ-08", "Chatbot AI", "Tích hợp Google Gemini AI hỗ trợ tư vấn học tiếng Trung.", "Trung bình"),
        ("REQ-09", "Quản lý hồ sơ Giáo viên", "Giáo viên cập nhật thông tin cá nhân, giờ dạy, mức phí.", "Trung bình"),
        ("REQ-10", "Quản lý đặt lịch", "Giáo viên xác nhận/từ chối yêu cầu từ học sinh.", "Cao"),
    ]
    add_table_with_header(doc,
        ["Mã", "Chức năng", "Mô tả", "Ưu tiên"],
        func_reqs)

    doc.add_paragraph()
    add_heading(doc, "2.2. Yêu cầu phi chức năng", level=2)
    nonfunc = [
        "Bảo mật: Mật khẩu được mã hoá bằng bcrypt. Token xác thực JWT với thời hạn 60 phút.",
        "Hiệu năng: API phản hồi dưới 500ms cho các thao tác thông thường.",
        "Giao diện: Responsive, hỗ trợ tốt trên màn hình 1024px trở lên.",
        "Khả năng mở rộng: Kiến trúc module hóa, dễ thêm tính năng mới.",
        "Tương thích: Hoạt động ổn định trên Chrome, Firefox, Edge.",
    ]
    for nf in nonfunc:
        p = doc.add_paragraph(nf, style="List Bullet")
        p.runs[0].font.size = Pt(11)

    doc.add_page_break()

    # ========== CHƯƠNG III: THIẾT KẾ HỆ THỐNG ==========
    add_heading(doc, "III. THIẾT KẾ HỆ THỐNG", level=1, color_hex="1F497D")

    add_heading(doc, "3.1. Sơ đồ kiến trúc hệ thống", level=2)
    add_para(doc, "Hệ thống Lanying HSK được xây dựng theo mô hình Client-Server 3 tầng: Giao diện người dùng (Frontend) – Máy chủ ứng dụng (Backend API) – Cơ sở dữ liệu.")
    doc.add_paragraph()
    add_image_safe(doc, ARCH_IMG, "Hình 1: Sơ đồ kiến trúc tổng thể hệ thống Lanying HSK", width=5.5)

    doc.add_paragraph()
    add_heading(doc, "3.2. Sơ đồ cơ sở dữ liệu (ER Diagram)", level=2)
    add_para(doc, "Cơ sở dữ liệu được thiết kế với 5 bảng chính, đảm bảo tính toàn vẹn dữ liệu và dễ mở rộng:")
    doc.add_paragraph()
    add_image_safe(doc, ER_IMG, "Hình 2: Sơ đồ quan hệ thực thể (ER) cơ sở dữ liệu", width=5.5)

    doc.add_paragraph()
    add_para(doc, "Mô tả các bảng chính:")
    db_tables = [
        ("users", "Lưu thông tin tài khoản người dùng (Học sinh & Giáo viên)", "id, name, email, password_hash, role, created_at"),
        ("tutors", "Hồ sơ chi tiết Giáo viên, chỉ tạo khi role = 'tutor'", "id, user_id(FK), bio, hsk_level, hourly_rate, is_active"),
        ("courses", "Khóa học do Giáo viên tạo ra", "id, tutor_id(FK), name, hsk_level, price, duration_weeks"),
        ("bookings", "Lịch đặt học giữa Học sinh và Giáo viên", "id, student_id(FK), tutor_id(FK), status, scheduled_at"),
        ("survey_responses", "Kết quả khảo sát lộ trình học của Học sinh", "id, user_id(FK), current_level, goals, skills, modes"),
    ]
    add_table_with_header(doc,
        ["Bảng", "Mô tả", "Các cột chính"],
        db_tables)

    doc.add_paragraph()
    add_heading(doc, "3.3. So do Use Case", level=2)
    add_para(doc, "So do Use Case mo ta cac chuc nang chinh cua he thong va cach cac tac nhan (actor) tuong tac voi he thong.")

    doc.add_paragraph()
    add_para(doc, "3.3.1. So do Use Case Dang nhap / Dang ky", bold=True)
    add_image_safe(doc, UC_AUTH, "Hinh 3: So do Use Case - Dang nhap va Dang ky", width=5.5)

    doc.add_paragraph()
    add_para(doc, "3.3.2. So do Use Case Hoc sinh", bold=True)
    add_image_safe(doc, UC_STUDENT, "Hinh 4: So do Use Case - Chuc nang Hoc sinh", width=5.5)

    doc.add_paragraph()
    add_para(doc, "3.3.3. So do Use Case Giao vien", bold=True)
    add_image_safe(doc, UC_TUTOR, "Hinh 5: So do Use Case - Chuc nang Giao vien", width=5.5)

    doc.add_paragraph()
    add_para(doc, "3.3.4. So do Use Case Dat lich va Quan ly lop", bold=True)
    add_image_safe(doc, UC_BOOKING, "Hinh 6: So do Use Case - Dat lich hoc va Quan ly lop", width=5.5)

    doc.add_page_break()

    add_heading(doc, "3.4. Phan quyen nguoi dung", level=2)
    add_para(doc, "Hệ thống có 2 loại tài khoản với quyền hạn và giao diện hoàn toàn riêng biệt:")
    perm_rows = [
        ("Học sinh (student)", "index.html", "Xem danh sách gia sư, khảo sát lộ trình, đặt lịch, chatbot AI", "Không"),
        ("Giáo viên (tutor)", "tutor_index.html", "Quản lý lớp học, duyệt/từ chối đặt lịch, cập nhật hồ sơ", "Bắt buộc HSK ≥ 5"),
    ]
    add_table_with_header(doc,
        ["Vai trò", "Trang chủ", "Chức năng", "Ràng buộc"],
        perm_rows)

    add_para(doc, "\nCơ chế redirect phân quyền:", bold=True)
    add_para(doc, "Khi đăng nhập, Backend trả về trường role trong JWT Token và dữ liệu JSON. Frontend JavaScript đọc role từ localStorage và tự động chuyển hướng: Giáo viên → tutor_index.html, Học sinh → index.html. Nếu Giáo viên cố tình truy cập trang Học sinh, code phát hiện và redirect trở lại trang Giáo viên ngay lập tức.")

    doc.add_page_break()

    # ========== CHƯƠNG IV: CÔNG NGHỆ ==========
    add_heading(doc, "IV. CÔNG NGHỆ SỬ DỤNG", level=1, color_hex="1F497D")
    tech_rows = [
        ("FastAPI (Python)", "Backend", "Framework Python hiệu năng cao cho REST API, tự động tạo Swagger docs"),
        ("SQLAlchemy", "ORM", "Object-Relational Mapper kết nối Python với SQLite database"),
        ("SQLite", "Database", "Hệ quản trị CSDL nhúng, phù hợp cho môi trường phát triển"),
        ("JWT (python-jose)", "Bảo mật", "JSON Web Token xác thực người dùng stateless"),
        ("bcrypt", "Bảo mật", "Thuật toán hash mật khẩu một chiều, chống brute-force"),
        ("HTML5 / CSS3", "Frontend", "Cấu trúc và giao diện web, responsive design"),
        ("JavaScript (Vanilla)", "Frontend", "Xử lý logic client-side, gọi API, phân quyền"),
        ("Google Gemini AI", "AI", "API trí tuệ nhân tạo tích hợp chatbot tư vấn học tiếng Trung"),
        ("uvicorn", "Server", "ASGI server chạy FastAPI backend"),
        ("python-docx", "Báo cáo", "Thư viện tạo file Word tự động từ Python"),
    ]
    add_table_with_header(doc,
        ["Công nghệ", "Tầng", "Mô tả"],
        tech_rows)

    doc.add_page_break()

    # ========== CHƯƠNG V: CÀI ĐẶT ==========
    add_heading(doc, "V. CÀI ĐẶT VÀ TRIỂN KHAI", level=1, color_hex="1F497D")

    add_heading(doc, "5.1. Yêu cầu môi trường", level=2)
    add_para(doc, "• Python 3.10 trở lên\n• pip (trình quản lý thư viện Python)\n• Trình duyệt hiện đại (Chrome, Firefox, Edge)\n• Kết nối Internet (để dùng Gemini AI chatbot)")

    add_heading(doc, "5.2. Các bước cài đặt", level=2)
    steps = [
        ("Bước 1", "Tải mã nguồn", "Giải nén hoặc clone project vào thư mục làm việc"),
        ("Bước 2", "Cài thư viện Python", "Chạy: pip install -r backend/requirements.txt"),
        ("Bước 3", "Khởi động Backend", "Vào thư mục backend, chạy: python -m uvicorn main:app --port 8000 --reload"),
        ("Bước 4", "Khởi động Frontend", "Vào thư mục gốc, chạy: python -m http.server 3000"),
        ("Bước 5", "Truy cập web", "Mở trình duyệt và vào địa chỉ: http://127.0.0.1:3000"),
    ]
    add_table_with_header(doc,
        ["", "Thao tác", "Chi tiết"],
        steps, header_bg="375623")

    add_heading(doc, "5.3. Cấu trúc thư mục dự án", level=2)
    tree_text = (
        "GiaSuTiengTrung/\n"
        "├── backend/\n"
        "│   ├── main.py              # Entry point FastAPI\n"
        "│   ├── database.py          # ORM Models (SQLAlchemy)\n"
        "│   ├── config.py            # Cấu hình JWT, database\n"
        "│   ├── requirements.txt     # Thư viện Python\n"
        "│   ├── lanyinghsk.db        # SQLite database file\n"
        "│   └── routers/\n"
        "│       ├── auth.py          # API đăng ký, đăng nhập\n"
        "│       ├── tutors.py        # API quản lý gia sư, đặt lịch\n"
        "│       ├── survey.py        # API khảo sát lộ trình\n"
        "│       └── chatbot.py       # API chatbot AI\n"
        "├── frontend/\n"
        "│   ├── pages/\n"
        "│   │   ├── login.html       # Trang đăng nhập / đăng ký\n"
        "│   │   ├── survey.html      # Trang khảo sát lộ trình\n"
        "│   │   ├── tutor_index.html # Dashboard giáo viên\n"
        "│   │   └── tutor_profile.html # Trang hồ sơ giáo viên\n"
        "│   └── js/\n"
        "│       └── api.js           # Wrapper gọi API backend\n"
        "├── index.html               # Trang chủ học sinh\n"
        "├── style.css                # CSS chung\n"
        "└── script.js                # JS chung\n"
    )
    p = doc.add_paragraph()
    run = p.add_run(tree_text)
    run.font.name = "Courier New"
    run.font.size = Pt(9)

    doc.add_page_break()

    # ========== CHƯƠNG VI: MÔ TẢ CHỨC NĂNG ==========
    add_heading(doc, "VI. MÔ TẢ CHỨC NĂNG CHI TIẾT", level=1, color_hex="1F497D")

    add_heading(doc, "6.1. Module Đăng nhập / Đăng ký", level=2)
    add_para(doc, "Trang login.html cung cấp form đăng nhập và đăng ký tích hợp. Người dùng chọn vai trò (Học sinh / Giáo viên) trước khi đăng ký. Hệ thống kiểm tra các ràng buộc:")
    reqs = [
        "Email phải chưa được đăng ký trong hệ thống.",
        "Mật khẩu được hash bằng bcrypt trước khi lưu vào CSDL.",
        "Giáo viên bắt buộc phải khai báo cấp độ HSK ≥ 5. Nếu HSK < 5, Backend trả về lỗi 400 và từ chối đăng ký.",
        "Sau khi đăng ký, Giáo viên được tự động kích hoạt (is_active=True) và hiển thị trong danh sách gia sư.",
        "Đăng nhập thành công trả về JWT Token, Frontend lưu vào localStorage và redirect đúng trang theo role.",
    ]
    for r in reqs:
        p = doc.add_paragraph(r, style="List Bullet")
        p.runs[0].font.size = Pt(11)

    add_heading(doc, "6.2. Module Học sinh", level=2)
    add_para(doc, "Sau khi đăng nhập, Học sinh được chuyển đến trang index.html với lời chào 'Xin chào Học sinh [Tên]'. Các chức năng bao gồm:")
    student_funcs = [
        "Xem danh sách Gia sư: Hiển thị tất cả gia sư đang hoạt động (is_active=True), có thể lọc theo cấp HSK.",
        "Xem chi tiết Gia sư: Thông tin hồ sơ, mức phí, chuyên môn, các khóa học đang mở.",
        "Đặt lịch học: Gửi yêu cầu đặt lịch đến Gia sư, kèm ghi chú.",
        "Khảo sát lộ trình học: Hoàn thành form khảo sát để nhận gợi ý lộ trình từ AI.",
        "Chatbot AI: Trò chuyện với Google Gemini AI về học tiếng Trung.",
    ]
    for sf in student_funcs:
        p = doc.add_paragraph(sf, style="List Bullet")
        p.runs[0].font.size = Pt(11)

    add_heading(doc, "6.3. Module Giáo viên", level=2)
    add_para(doc, "Sau khi đăng nhập, Giáo viên được chuyển đến trang tutor_index.html với lời chào 'Xin chào Giáo viên [Tên]'. Dashboard giáo viên KHÔNG có nút Khảo sát lộ trình. Các chức năng bao gồm:")
    tutor_funcs = [
        "Xem danh sách đặt lịch: Tất cả yêu cầu từ Học sinh, hiển thị tên, trạng thái, thời gian.",
        "Duyệt / Từ chối đặt lịch: Cập nhật trạng thái booking (pending → confirmed / cancelled).",
        "Cập nhật hồ sơ: Chỉnh sửa Bio, Mức phí, Chuyên môn.",
        "Bảo vệ trang: Nếu tài khoản không phải Giáo viên truy cập trang này, hệ thống redirect về trang đăng nhập.",
    ]
    for tf in tutor_funcs:
        p = doc.add_paragraph(tf, style="List Bullet")
        p.runs[0].font.size = Pt(11)

    add_heading(doc, "6.4. Module Khảo sát lộ trình học", level=2)
    add_para(doc, "Chỉ dành cho Học sinh. Gồm 5 bước khảo sát: Trình độ hiện tại → Mục tiêu học → Kỹ năng cần phát triển → Hình thức học → Thông tin cá nhân. Kết quả được gửi lên Backend, lưu vào bảng survey_responses và AI phân tích để trả về lộ trình học phù hợp.")

    add_heading(doc, "6.5. Module Đặt lịch gia sư", level=2)
    booking_flow = [
        ("Học sinh", "Chọn gia sư từ danh sách, bấm nút Đặt lịch"),
        ("Hệ thống", "Gửi POST /api/tutors/{id}/book với JWT Token"),
        ("Backend", "Tạo bản ghi Booking với status='pending'"),
        ("Giáo viên", "Thấy booking mới trong Dashboard"),
        ("Giáo viên", "Bấm Xác nhận → PUT /api/tutors/bookings/{id} → status='confirmed'"),
        ("Học sinh", "Xem trạng thái đặt lịch trong Dashboard"),
    ]
    add_table_with_header(doc, ["Tác nhân", "Hành động"], booking_flow, header_bg="7030A0")

    doc.add_page_break()

    # ========== CHƯƠNG VII: API BACKEND ==========
    add_heading(doc, "VII. MÔ TẢ API BACKEND", level=1, color_hex="1F497D")
    add_para(doc, "Backend sử dụng FastAPI, tự động tạo tài liệu Swagger tại http://127.0.0.1:8000/docs. Dưới đây là danh sách các API chính:")

    api_rows = [
        ("POST", "/api/auth/register", "Đăng ký tài khoản mới (student/tutor)", "Không"),
        ("POST", "/api/auth/login", "Đăng nhập, trả về JWT Token", "Không"),
        ("GET", "/api/auth/me/dashboard", "Lấy thông tin Dashboard theo role", "JWT"),
        ("GET", "/api/tutors/", "Lấy danh sách gia sư (có filter HSK)", "Không"),
        ("GET", "/api/tutors/{id}", "Lấy chi tiết một gia sư", "Không"),
        ("POST", "/api/tutors/{id}/book", "Học sinh đặt lịch gia sư", "JWT"),
        ("PUT", "/api/tutors/bookings/{id}", "Giáo viên duyệt/từ chối lịch", "JWT"),
        ("GET", "/api/tutors/me", "Giáo viên xem hồ sơ của mình", "JWT"),
        ("PUT", "/api/tutors/me", "Giáo viên cập nhật hồ sơ", "JWT"),
        ("POST", "/api/survey/", "Học sinh gửi kết quả khảo sát", "JWT"),
        ("POST", "/api/chatbot/", "Gửi tin nhắn đến Gemini AI", "JWT"),
    ]
    add_table_with_header(doc,
        ["Phương thức", "Endpoint", "Mô tả", "Xác thực"],
        api_rows)

    doc.add_paragraph()
    add_para(doc, "Cơ chế bảo mật JWT:", bold=True)
    add_para(doc, "Mỗi request đến API cần xác thực phải kèm header: Authorization: Bearer <token>. Backend giải mã token bằng SECRET_KEY, lấy user_id và role để kiểm tra quyền. Token có hiệu lực 60 phút kể từ thời điểm đăng nhập.")

    doc.add_page_break()

    # ========== CHƯƠNG VIII: KẾT QUẢ ==========
    add_heading(doc, "VIII. KẾT QUẢ ĐẠT ĐƯỢC", level=1, color_hex="1F497D")

    add_heading(doc, "8.1. Chức năng hoàn thành", level=2)
    done_features = [
        ("✅", "Hệ thống đăng ký / đăng nhập phân quyền", "Hoàn thành 100%"),
        ("✅", "Trang chủ riêng biệt cho Học sinh", "Hoàn thành 100%"),
        ("✅", "Trang Dashboard riêng cho Giáo viên", "Hoàn thành 100%"),
        ("✅", "Ràng buộc HSK ≥ 5 cho Giáo viên", "Hoàn thành 100%"),
        ("✅", "Danh sách Gia sư với thông tin đầy đủ", "Hoàn thành 100%"),
        ("✅", "Module đặt lịch và quản lý booking", "Hoàn thành 100%"),
        ("✅", "Khảo sát lộ trình học AI-powered", "Hoàn thành 100%"),
        ("✅", "Chatbot Google Gemini AI", "Hoàn thành 100%"),
        ("✅", "REST API với FastAPI + Swagger docs", "Hoàn thành 100%"),
        ("✅", "Cơ sở dữ liệu SQLite với 5 bảng", "Hoàn thành 100%"),
        ("⏳", "Tích hợp cổng thanh toán", "Chưa thực hiện (scope mở rộng)"),
        ("⏳", "Ứng dụng di động (iOS/Android)", "Chưa thực hiện (scope mở rộng)"),
    ]
    add_table_with_header(doc,
        ["", "Chức năng", "Tình trạng"],
        done_features)

    add_heading(doc, "8.2. Kiểm thử hệ thống", level=2)
    test_rows = [
        ("TC-01", "Đăng ký tài khoản Học sinh", "Thành công", "Pass"),
        ("TC-02", "Đăng ký Giáo viên HSK < 5", "Từ chối với lỗi 400", "Pass"),
        ("TC-03", "Đăng ký Giáo viên HSK = 5", "Thành công, hiện lên danh sách", "Pass"),
        ("TC-04", "Đăng nhập Học sinh, redirect đúng trang", "index.html, lời chào Học sinh", "Pass"),
        ("TC-05", "Đăng nhập Giáo viên, redirect đúng trang", "tutor_index.html, lời chào Giáo viên", "Pass"),
        ("TC-06", "Giáo viên cố truy cập trang Học sinh", "Redirect về tutor_index.html", "Pass"),
        ("TC-07", "Học sinh đặt lịch Giáo viên", "Booking tạo thành công, status=pending", "Pass"),
        ("TC-08", "Giáo viên xác nhận booking", "Status cập nhật thành confirmed", "Pass"),
        ("TC-09", "Chatbot AI phản hồi câu hỏi", "Gemini trả về gợi ý học", "Pass"),
        ("TC-10", "Token hết hạn, truy cập API bảo vệ", "Lỗi 401, redirect về login", "Pass"),
    ]
    add_table_with_header(doc,
        ["Mã TC", "Mô tả test", "Kết quả mong đợi", "Kết quả"],
        test_rows, header_bg="833C00")

    doc.add_page_break()

    # ========== CHƯƠNG IX: KẾT LUẬN ==========
    add_heading(doc, "IX. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", level=1, color_hex="1F497D")

    add_heading(doc, "9.1. Kết luận", level=2)
    add_para(doc, "Dự án \"Nền tảng Gia sư Tiếng Trung Trực tuyến – Lanying HSK\" đã hoàn thành thành công các mục tiêu đề ra ban đầu. Hệ thống cung cấp một nền tảng kết nối học sinh và gia sư tiếng Trung chuyên nghiệp, với đầy đủ các tính năng cốt lõi: phân quyền rõ ràng, đặt lịch học, khảo sát lộ trình AI, và chatbot tư vấn thông minh.")
    add_para(doc, "Điểm nổi bật của dự án là cơ chế đảm bảo chất lượng giảng dạy: chỉ cho phép gia sư đạt chứng chỉ HSK cấp 5 trở lên được đăng ký giảng dạy trên nền tảng. Điều này đảm bảo học sinh được học với những gia sư có trình độ thực sự vững chắc.")
    add_para(doc, "Về mặt kỹ thuật, dự án áp dụng thành công các công nghệ hiện đại: FastAPI (Python) cho backend, JWT authentication, SQLAlchemy ORM, và tích hợp Google Gemini AI – thể hiện khả năng vận dụng kiến thức trong môi trường thực tế.")

    add_heading(doc, "9.2. Hướng phát triển trong tương lai", level=2)
    future = [
        "Tích hợp cổng thanh toán trực tuyến (VNPay, MoMo) để xử lý học phí.",
        "Xây dựng ứng dụng di động iOS/Android bằng React Native hoặc Flutter.",
        "Thêm tính năng đánh giá và nhận xét sau mỗi buổi học.",
        "Tích hợp video call trực tiếp trong nền tảng (WebRTC).",
        "Triển khai hệ thống gợi ý gia sư thông minh hơn bằng Machine Learning.",
        "Mở rộng sang các ngôn ngữ khác: tiếng Nhật, tiếng Hàn.",
        "Triển khai lên môi trường production (Docker + Cloud: AWS/GCP/Azure).",
    ]
    for f in future:
        p = doc.add_paragraph(f, style="List Bullet")
        p.runs[0].font.size = Pt(11)

    add_heading(doc, "9.3. Bài học kinh nghiệm", level=2)
    lessons = [
        "Việc thiết kế cơ sở dữ liệu tốt từ đầu giúp tránh nhiều vấn đề phát sinh sau này.",
        "Phân quyền người dùng cần được xử lý cả ở Frontend lẫn Backend để đảm bảo an toàn.",
        "Tích hợp AI API (Gemini) tương đối dễ dàng nhờ SDK chính thức của Google.",
        "FastAPI là framework tốt cho việc xây dựng REST API nhanh chóng với Python.",
        "Quản lý JWT Token đúng cách (lưu, kiểm tra, xóa khi logout) rất quan trọng cho UX.",
    ]
    for l in lessons:
        p = doc.add_paragraph(l, style="List Bullet")
        p.runs[0].font.size = Pt(11)

    # ========== TÀI LIỆU THAM KHẢO ==========
    doc.add_page_break()
    add_heading(doc, "TÀI LIỆU THAM KHẢO", level=1, color_hex="1F497D")
    refs = [
        "[1] FastAPI Official Documentation. https://fastapi.tiangolo.com/",
        "[2] SQLAlchemy Documentation. https://docs.sqlalchemy.org/",
        "[3] Python-Jose JWT Library. https://python-jose.readthedocs.io/",
        "[4] Google Gemini AI API Documentation. https://ai.google.dev/",
        "[5] HSK (Hanyu Shuiping Kaoshi) Official Website. http://www.chinesetest.cn/",
        "[6] MDN Web Docs – HTML, CSS, JavaScript. https://developer.mozilla.org/",
        "[7] bcrypt Password Hashing Library. https://pypi.org/project/bcrypt/",
        "[8] python-docx Library. https://python-docx.readthedocs.io/",
    ]
    for ref in refs:
        p = doc.add_paragraph(ref)
        p.runs[0].font.size = Pt(11)
        p.paragraph_format.space_after = Pt(3)

    # ========== LƯU FILE ==========
    out = BASE / "FullProjectReport_LanyingHSK.docx"
    doc.save(str(out))
    print("[OK] Bao cao da duoc tao thanh cong: " + str(out))
    print("   Kich thuoc: " + str(round(out.stat().st_size / 1024, 1)) + " KB")

if __name__ == "__main__":
    main()
