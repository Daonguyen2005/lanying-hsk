from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers import auth, tutors, survey, chatbot
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: tạo tables khi server khởi động
    try:
        from database import Base, engine
        Base.metadata.create_all(bind=engine)
        print("[OK] Database tables ready!")
    except Exception as e:
        print(f"[WARNING] DB Warning: {e}")
    yield
    # Shutdown
    print("Server shutting down...")

app = FastAPI(
    title="Lanying HSK API",
    description="Backend API cho nền tảng gia sư tiếng Trung Lanying HSK",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(tutors.router)
app.include_router(survey.router)
app.include_router(chatbot.router)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/frontend", StaticFiles(directory=os.path.join(BASE_DIR, "frontend")), name="frontend")

@app.get("/")
def root():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/{filename}")
def serve_root_files(filename: str):
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
