// =============================================
// API.JS - Tập trung xử lý tất cả HTTP request
// Backend URL: http://localhost:8000
// =============================================

const API_BASE = "";

function getToken() {
    return localStorage.getItem("lanying_token");
}

function getUser() {
    const u = localStorage.getItem("lanying_user");
    return u ? JSON.parse(u) : null;
}

async function apiRequest(endpoint, method = "GET", body = null) {
    const headers = { "Content-Type": "application/json" };
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const options = { method, headers };
    if (body) options.body = JSON.stringify(body);

    const res = await fetch(`${API_BASE}${endpoint}`, options);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Có lỗi xảy ra");
    return data;
}

// Auth APIs
const AuthAPI = {
    register: (name, email, password, role = "student", hsk_level = 1, specialization = "") =>
        apiRequest("/api/auth/register", "POST", { name, email, password, role, hsk_level, specialization }),
    login: (email, password) =>
        apiRequest("/api/auth/login", "POST", { email, password }),
    getDashboard: () => apiRequest("/api/auth/me/dashboard")
};

// Tutor APIs
const TutorAPI = {
    getAll: (hsk_level = null) =>
        apiRequest(`/api/tutors/${hsk_level ? `?hsk_level=${hsk_level}` : ""}`),
    getById: (id) => apiRequest(`/api/tutors/${id}`),
    getMyProfile: () => apiRequest("/api/tutors/me"),
    updateMyProfile: (data) => apiRequest("/api/tutors/me", "PUT", data),
    book: (id, note = "") => apiRequest(`/api/tutors/${id}/book`, "POST", { note }),
    updateBookingStatus: (id, status) => apiRequest(`/api/tutors/bookings/${id}`, "PUT", { status })
};

// Survey API
const SurveyAPI = {
    submit: (data) => apiRequest("/api/survey/", "POST", data),
};

// Chatbot API
const ChatAPI = {
    send: (message) => apiRequest("/api/chat/", "POST", { message }),
};
