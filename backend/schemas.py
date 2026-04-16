"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, List, Any
from datetime import datetime


# ─── Auth Schemas ───────────────────────────────────────────

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email: str


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


# ─── Upload Schemas ─────────────────────────────────────────

class UploadResponse(BaseModel):
    filename: str
    extracted_text: str
    page_count: int
    char_count: int


# ─── Analysis Schemas ───────────────────────────────────────

class AnalysisRequest(BaseModel):
    extracted_text: str = Field(..., min_length=50)
    filename: Optional[str] = "untitled.pdf"


class SwotAnalysis(BaseModel):
    strengths: List[str] = []
    weaknesses: List[str] = []
    opportunities: List[str] = []
    threats: List[str] = []


class ScoreBreakdown(BaseModel):
    market_potential: Optional[int] = None
    team_strength: Optional[int] = None
    innovation: Optional[int] = None
    financial_viability: Optional[int] = None
    scalability: Optional[int] = None
    reasoning: Optional[str] = None


class AnalysisResponse(BaseModel):
    id: int
    viability_score: float
    swot_analysis: Dict[str, Any]
    detailed_analysis: str
    score_breakdown: Optional[Dict[str, Any]] = None
    pitch_filename: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisListItem(BaseModel):
    id: int
    score: Optional[float]
    pitch_filename: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
