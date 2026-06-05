import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config

from app.database import engine
from app.models import Base
from app.routers import auth, chat, reports

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Chatbot API",
    description="Backend API for AI Chatbot with Gemini integration",
    version="1.0.0"
)

# CORS middleware
allowed_origins = [
    config("FRONTEND_URL", default="http://localhost:5173"),
]

# Add additional allowed origins from environment variable
additional_origins = config("ADDITIONAL_ALLOWED_ORIGINS", default="").split(",")
allowed_origins.extend([origin.strip() for origin in additional_origins if origin.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(reports.router, tags=["reports"])

@app.get("/")
async def root():
    return {"message": "AI Chatbot API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Serve React frontend in production
# Check if the dist directory exists (created by npm run build)
static_dir = os.path.join(os.path.dirname(__file__), "..", "dist")
if os.path.exists(static_dir):
    # Mount static files (js, css, assets)
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")
    
    # Catch-all route to serve index.html for SPA routing
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Prevent catching API routes
        if full_path.startswith("auth/") or full_path.startswith("chat/") or full_path.startswith("reports/") or full_path.startswith("api/"):
            return {"detail": "Not Found"}
            
        file_path = os.path.join(static_dir, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(static_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
