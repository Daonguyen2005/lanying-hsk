-- ============================================
-- LANYING HSK - DATABASE SCHEMA (SQL Server)
-- ============================================

-- Tạo Database
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'LanyingHSK')
BEGIN
    CREATE DATABASE LanyingHSK;
END
GO

USE LanyingHSK;
GO

-- Bảng 1: Người dùng
CREATE TABLE users (
    id          INT PRIMARY KEY IDENTITY(1,1),
    name        NVARCHAR(100) NOT NULL,
    email       NVARCHAR(150) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    role        NVARCHAR(20) DEFAULT 'student' CHECK (role IN ('student','tutor','admin')),
    created_at  DATETIME DEFAULT GETDATE()
);
GO

-- Bảng 2: Hồ sơ Gia sư
CREATE TABLE tutors (
    id              INT PRIMARY KEY IDENTITY(1,1),
    user_id         INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    bio             NVARCHAR(MAX),
    hsk_level       INT CHECK (hsk_level BETWEEN 1 AND 6),
    hourly_rate     DECIMAL(10,2),
    specialization  NVARCHAR(255),
    -- Tags lưu dưới dạng JSON string để tính Cosine Similarity
    -- VD: {"goal_hsk":1,"goal_comm":0,"goal_biz":0,"level_beginner":1,"online":1,"offline":0}
    tags_vector     NVARCHAR(500),
    is_active       BIT DEFAULT 1,
    created_at      DATETIME DEFAULT GETDATE()
);
GO

-- Bảng 3: Khóa học
CREATE TABLE courses (
    id              INT PRIMARY KEY IDENTITY(1,1),
    tutor_id        INT REFERENCES tutors(id),
    name            NVARCHAR(200) NOT NULL,
    hsk_level       INT CHECK (hsk_level BETWEEN 1 AND 6),
    description     NVARCHAR(MAX),
    price           DECIMAL(10,2),
    duration_weeks  INT,
    is_active       BIT DEFAULT 1,
    created_at      DATETIME DEFAULT GETDATE()
);
GO

-- Bảng 4: Đặt lịch học
CREATE TABLE bookings (
    id              INT PRIMARY KEY IDENTITY(1,1),
    student_id      INT NOT NULL REFERENCES users(id),
    tutor_id        INT NOT NULL REFERENCES tutors(id),
    course_id       INT REFERENCES courses(id),
    scheduled_at    DATETIME NOT NULL,
    duration_hours  INT DEFAULT 1,
    status          NVARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending','confirmed','cancelled','completed')),
    note            NVARCHAR(500),
    created_at      DATETIME DEFAULT GETDATE()
);
GO

-- Bảng 5: Kết quả khảo sát (Cosine Similarity)
CREATE TABLE survey_responses (
    id              INT PRIMARY KEY IDENTITY(1,1),
    user_id         INT REFERENCES users(id),
    current_level   NVARCHAR(50),   -- 'beginner','hsk1','hsk2','hsk3','hsk4'
    goal            NVARCHAR(50),   -- 'hsk_exam','communication','business'
    time_per_week   INT,            -- Số giờ/tuần có thể học
    prefer_online   BIT,
    created_at      DATETIME DEFAULT GETDATE()
);
GO

-- =============================================
-- DỮ LIỆU MẪU (Seed Data)
-- =============================================

-- Admin account (password: admin123)
INSERT INTO users (name, email, password_hash, role) VALUES
(N'Quản trị viên', 'admin@lanyinghsk.com', '$2b$12$examplehashforadmin', 'admin');

-- Tài khoản gia sư
INSERT INTO users (name, email, password_hash, role) VALUES
(N'Lý Minh', 'lyminh@lanyinghsk.com', '$2b$12$examplehashfortutor1', 'tutor'),
(N'Trần Phong', 'tranphong@lanyinghsk.com', '$2b$12$examplehashfortutor2', 'tutor'),
(N'Nguyễn Hoa', 'nguyenhoa@lanyinghsk.com', '$2b$12$examplehashfortutor3', 'tutor');

-- Hồ sơ gia sư
INSERT INTO tutors (user_id, bio, hsk_level, hourly_rate, specialization, tags_vector) VALUES
(2, N'10 năm kinh nghiệm luyện thi HSK 5-6, từng đạt HSK 6 tại Bắc Kinh', 6, 150000, N'Luyện thi HSK, Giao tiếp', '{"goal_hsk":1,"goal_comm":1,"goal_biz":0,"level_beginner":0,"level_intermediate":0,"level_advanced":1,"online":1,"offline":0}'),
(3, N'Chuyên gia sư tiếng Trung thương mại, kinh nghiệm làm việc tại Đài Loan', 5, 120000, N'Tiếng Trung thương mại, HSK 3-4', '{"goal_hsk":1,"goal_comm":1,"goal_biz":1,"level_beginner":0,"level_intermediate":1,"level_advanced":0,"online":1,"offline":1}'),
(4, N'Gia sư nhẹ nhàng, chuyên dạy người mới bắt đầu, phát âm chuẩn', 4, 80000, N'Sơ cấp, Phát âm', '{"goal_hsk":0,"goal_comm":1,"goal_biz":0,"level_beginner":1,"level_intermediate":0,"level_advanced":0,"online":0,"offline":1}');

-- Khóa học mẫu
INSERT INTO courses (tutor_id, name, hsk_level, description, price, duration_weeks) VALUES
(1, N'Luyện thi HSK 6 - Cấp tốc', 6, N'Khóa học dành cho học viên muốn thi HSK 6 trong 3 tháng', 3000000, 12),
(2, N'Tiếng Trung Thương Mại HSK 4', 4, N'Học từ vựng và giao tiếp trong môi trường doanh nghiệp', 2000000, 8),
(3, N'Tiếng Trung Nhập Môn - Phát âm chuẩn', 1, N'Học từ đầu, phát âm 4 thanh điệu chuẩn xác', 800000, 4);
GO
