
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Optional, Literal
from ..models.data_models import ParsedQuery, Desk, QueryInput # <-- Import QueryInput
from ..services.llm_service import LLMService
from ..services.recommendation_service import RecommendationService

router = APIRouter()

# Dependencies
def get_llm_service():
    return LLMService()

def get_recommendation_service(llm_service: LLMService = Depends(get_llm_service)):
    return RecommendationService(llm_service)

@router.post("/query-occupancy", response_model=List[Desk], summary="Query available workspaces using natural language")
async def query_occupancy(
    query_input: QueryInput, # <-- Change this parameter
    rec_service: RecommendationService = Depends(get_recommendation_service)
):
    """
    Receives a natural language query for workspace allocation and returns matching recommendations.
    """
    query_text = query_input.query_text # <-- Access the query text from the model

    try:
        recommendations = await rec_service.find_available_desks(query_text)
        if not recommendations:
            return []
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
    
# Optional: testing/inspection
@router.get("/data/spaces")
async def get_all_spaces():
    from ..services.data_loader import data_loader
    return data_loader.get_spaces()

@router.get("/data/desks")
async def get_all_desks():
    from ..services.data_loader import data_loader
    return data_loader.get_desks()
