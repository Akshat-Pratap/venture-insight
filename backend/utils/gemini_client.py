"""
Google Gemini API integration for startup analysis.
"""

import os
import json
import re
import hashlib
from typing import Optional, Dict, Any, List
from functools import lru_cache
   
import google.generativeai as genai
from dotenv import load_dotenv
 
# ─── Configuration ──────────────────────────────────────────
load_dotenv()
 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
 
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemma-4-31b-it")

# Simple in-memory cache for analysis results
_analysis_cache: Dict[str, Dict[str, Any]] = {}
MAX_CACHE_SIZE = 50


def _get_cache_key(text: str) -> str:
    """Generate a cache key from the input text."""
    return hashlib.md5(text[:2000].encode()).hexdigest()


def build_analysis_prompt(pitch_text: str, historical_data: List[Dict[str, Any]]) -> str:
    """
    Construct a structured prompt for Gemini analysis.

    Args:
        pitch_text: Extracted text from the pitch deck PDF.
        historical_data: List of historical startup records for comparison.

    Returns:
        Formatted prompt string.
    """
    historical_section = ""
    for startup in historical_data:
        historical_section += (
            f"- {startup['name']} ({startup['industry']}): "
            f"Funding: {startup['funding']}, Outcome: {startup['outcome']}. "
            f"{startup['description']}\n"
        )

    prompt = f"""Analyze the following startup pitch in a highly critical and realistic manner.
You must act as an experienced venture capitalist with 20+ years of experience.
Be brutally honest and data-driven in your assessment.

Return your analysis in the following JSON format ONLY (no markdown, no code fences, just raw JSON):
{{
    "viability_score": <number 0-100>,
    "score_breakdown": {{
        "market_potential": <number 0-100>,
        "team_strength": <number 0-100>,
        "innovation": <number 0-100>,
        "financial_viability": <number 0-100>,
        "scalability": <number 0-100>,
        "reasoning": "<brief explanation of why this overall score was given>"
    }},
    "swot_analysis": {{
        "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
        "weaknesses": ["<weakness 1>", "<weakness 2>", "<weakness 3>"],
        "opportunities": ["<opportunity 1>", "<opportunity 2>", "<opportunity 3>"],
        "threats": ["<threat 1>", "<threat 2>", "<threat 3>"]
    }},
    "detailed_analysis": "<comprehensive multi-paragraph analysis covering: market analysis, competitive landscape, business model evaluation, risk factors, team assessment, and growth potential. Be detailed and specific, at least 300 words.>",
    "comparison_with_historical": "<compare this startup with 2-3 similar historical startups from the data provided, noting patterns of success or failure>"
}}

IMPORTANT RULES:
1. The viability_score must be realistic - most startups should score between 25-65
2. Only truly exceptional pitches should score above 75
3. Be specific in your SWOT analysis - avoid generic statements
4. Reference specific details from the pitch in your analysis
5. The detailed_analysis must be comprehensive, at least 300 words

Startup Pitch:
{pitch_text[:6000]}

Historical Startup Data for Comparison:
{historical_section}
"""
    return prompt


async def analyze_startup(
    pitch_text: str,
    historical_data: List[Dict[str, Any]],
    max_retries: int = 3
) -> Dict[str, Any]:
    """
    Send pitch text to Gemini API for analysis with retry logic.

    Args:
        pitch_text: Extracted text from pitch deck.
        historical_data: Historical startup records for context.
        max_retries: Number of retry attempts on failure.

    Returns:
        Parsed analysis results dictionary.
    """
    # Check cache
    cache_key = _get_cache_key(pitch_text)
    if cache_key in _analysis_cache:
        return _analysis_cache[cache_key]

    prompt = build_analysis_prompt(pitch_text, historical_data)

    last_error = None
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            result_text = response.text

            # Parse the JSON response
            parsed = _parse_gemini_response(result_text)

            # Cache the result
            if len(_analysis_cache) >= MAX_CACHE_SIZE:
                # Remove oldest entry
                oldest_key = next(iter(_analysis_cache))
                del _analysis_cache[oldest_key]
            _analysis_cache[cache_key] = parsed

            return parsed

        except json.JSONDecodeError as e:
            last_error = f"JSON parsing error on attempt {attempt + 1}: {str(e)}"
            continue
        except Exception as e:
            last_error = f"API error on attempt {attempt + 1}: {str(e)}"
            if attempt < max_retries - 1:
                continue

    # All retries failed — return a structured fallback
    return _get_fallback_response(last_error)


def _parse_gemini_response(response_text: str) -> Dict[str, Any]:
    """Parse and validate the Gemini API response."""
    # Try to extract JSON from the response
    text = response_text.strip()

    # Remove markdown code fences if present
    if text.startswith("```"):
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)

    # Try direct JSON parse
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON object in the text
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            data = json.loads(json_match.group())
        else:
            raise json.JSONDecodeError("No valid JSON found in response", text, 0)

    # Validate required fields
    result = {
        "viability_score": _clamp(data.get("viability_score", 50), 0, 100),
        "score_breakdown": data.get("score_breakdown", {}),
        "swot_analysis": _validate_swot(data.get("swot_analysis", {})),
        "detailed_analysis": data.get("detailed_analysis", "Analysis not available."),
    }

    # Append historical comparison to detailed analysis if present
    comparison = data.get("comparison_with_historical", "")
    if comparison:
        result["detailed_analysis"] += f"\n\n**Historical Comparison:**\n{comparison}"

    return result


def _validate_swot(swot: Dict) -> Dict:
    """Ensure SWOT has all four categories with lists."""
    return {
        "strengths": swot.get("strengths", ["Not available"]),
        "weaknesses": swot.get("weaknesses", ["Not available"]),
        "opportunities": swot.get("opportunities", ["Not available"]),
        "threats": swot.get("threats", ["Not available"]),
    }


def _clamp(value, min_val, max_val):
    """Clamp a numeric value to a range."""
    try:
        return max(min_val, min(max_val, float(value)))
    except (TypeError, ValueError):
        return 50


def _get_fallback_response(error_msg: str) -> Dict[str, Any]:
    """Return a structured fallback when the API fails."""
    return {
        "viability_score": 0,
        "score_breakdown": {
            "market_potential": 0,
            "team_strength": 0,
            "innovation": 0,
            "financial_viability": 0,
            "scalability": 0,
            "reasoning": f"Analysis failed after multiple retries. Error: {error_msg}"
        },
        "swot_analysis": {
            "strengths": ["Unable to analyze"],
            "weaknesses": ["Unable to analyze"],
            "opportunities": ["Unable to analyze"],
            "threats": ["Unable to analyze"]
        },
        "detailed_analysis": (
            f"The AI analysis could not be completed. Error: {error_msg}. "
            "Please try again later or contact support."
        ),
    }
