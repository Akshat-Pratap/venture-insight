"""
Analysis routes: trigger AI analysis, retrieve history.
"""

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User, Analysis, StartupHistorical
from schemas import AnalysisRequest, AnalysisResponse, AnalysisListItem
from auth import get_current_user
from utils.gemini_client import analyze_startup

router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post("/analyze", response_model=AnalysisResponse)
async def run_analysis(
    data: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze startup pitch text using Gemini AI.
    Fetches historical data, constructs prompt, parses response, saves to DB.
    """
    # Fetch historical startup data for comparison
    historical_startups = db.query(StartupHistorical).all()
    historical_data = [
        {
            "name": s.name,
            "industry": s.industry,
            "funding": s.funding,
            "outcome": s.outcome,
            "description": s.description,
        }
        for s in historical_startups
    ]

    # Call Gemini API
    try:
        result = await analyze_startup(
            pitch_text=data.extracted_text,
            historical_data=historical_data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI analysis service error: {str(e)}"
        )

    # Save analysis to database
    analysis = Analysis(
        user_id=current_user.id,
        pitch_filename=data.filename,
        score=result.get("viability_score", 0),
        swot=result.get("swot_analysis", {}),
        analysis_text=result.get("detailed_analysis", ""),
        score_breakdown=result.get("score_breakdown", {}),
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return AnalysisResponse(
        id=analysis.id,
        viability_score=analysis.score,
        swot_analysis=analysis.swot,
        detailed_analysis=analysis.analysis_text,
        score_breakdown=analysis.score_breakdown,
        pitch_filename=analysis.pitch_filename,
        created_at=analysis.created_at
    )


@router.get("/analyses", response_model=List[AnalysisListItem])
def list_analyses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all analyses for the current user, most recent first."""
    analyses = (
        db.query(Analysis)
        .filter(Analysis.user_id == current_user.id)
        .order_by(Analysis.created_at.desc())
        .all()
    )

    return [
        AnalysisListItem(
            id=a.id,
            score=a.score,
            pitch_filename=a.pitch_filename,
            created_at=a.created_at
        )
        for a in analyses
    ]


@router.get("/analyses/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific analysis by ID (must belong to current user)."""
    analysis = (
        db.query(Analysis)
        .filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id)
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )

    return AnalysisResponse(
        id=analysis.id,
        viability_score=analysis.score,
        swot_analysis=analysis.swot or {},
        detailed_analysis=analysis.analysis_text or "",
        score_breakdown=analysis.score_breakdown,
        pitch_filename=analysis.pitch_filename,
        created_at=analysis.created_at
    )
