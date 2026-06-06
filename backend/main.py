import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decouple import config

from app.database import engine
from app.models import Base
from app.routers import auth, chat, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Chatbot API",
    description="Backend API for AI Chatbot with Gemini integration",
    version="1.0.0"
)

allowed_origins = [
    config("FRONTEND_URL", default="http://localhost:5173"),
]

additional_origins = config("ADDITIONAL_ALLOWED_ORIGINS", default="").split(",")
allowed_origins.extend([origin.strip() for origin in additional_origins if origin.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(reports.router, tags=["reports"])

@app.get("/")
async def root():
    return {"message": "AI Chatbot API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
