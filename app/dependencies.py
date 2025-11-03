from fastapi import Request, HTTPException, status, Depends
from app.services.model_services import ModelService

# Dependency to extract HF token from Authorization header
def get_hf_token(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header"
            )
        token = auth_header.split("Bearer ")[1]
        return token
    except  Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error processing Authorization header"
        ) from e
    
def get_model_service(hf_token: str = Depends(get_hf_token)) -> ModelService:
    """FastAPI dependency that provides a configured ModelService.

    This depends on `get_hf_token` so route handlers that depend on
    `get_model_service` don't need to extract the token themselves.
    """
    return ModelService(hf_token=hf_token)