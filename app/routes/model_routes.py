from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.responses import JSONResponse
from app import get_hf_token
from app.services import ModelService
import logging
logger = logging.getLogger(__name__)

router=APIRouter()


@router.post("/model-response")
async def get_response(request:Request, hf_token: str = Depends(get_hf_token)):
    try:
        data = await request.json()
        prompt = data.get("prompt")
        model = data.get("model")
        provider = data.get("provider")
        
        model_service = ModelService(
            model=model,
            hf_token=hf_token,
            provider=provider)
        
        try:
            response = model_service.generate_text(prompt)
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        
        return JSONResponse(content=response)
    except RuntimeError as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")