"""
Venture Insight — FastAPI Application Entry Point.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import init_db
from routes import auth_routes, upload_routes, analysis_routes

# Load environment variables at the entry point
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    init_db()
    yield


app = FastAPI(
    title="Venture Insight API",
    description="AI-powered startup pitch deck analysis platform",
    version="1.0.0",
    lifespan=lifespan
)

# ─── CORS Middleware ────────────────────────────────────────


  

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://venture-insight.vercel.app", # Your production frontend
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Include Routers ────────────────────────────────────────

app.include_router(auth_routes.router)
app.include_router(upload_routes.router)
app.include_router(analysis_routes.router)


@app.get("/")
def root():
    return {
        "app": "Venture Insight",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
