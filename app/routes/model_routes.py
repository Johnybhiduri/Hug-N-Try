from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.responses import JSONResponse
from app.dependencies import get_model_service
from app.services.model_services import ModelService
import logging
logger = logging.getLogger(__name__)

router=APIRouter()


@router.post("/model-response")
async def get_response(request: Request, model_service: ModelService = Depends(get_model_service)):
    try:
        data = await request.json()
        prompt = data.get("prompt")
        model = data.get("model")

        try:
            response = model_service.generate_text(prompt, model)
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise HTTPException(status_code=400, detail=str(e))

        return JSONResponse(content=response)
    except RuntimeError as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/served-models")
async def get_served_models(model_service: ModelService = Depends(get_model_service)):
    try:
        models = model_service.list_served_models()
        return JSONResponse(content={"served_models": models})
    except RuntimeError as e:
        logger.error(f"Error fetching served models: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")