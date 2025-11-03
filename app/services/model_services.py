from huggingface_hub.utils import (
    HfHubHTTPError,
    # RepositoryNotFoundError,
    # HfHubAuthenticationError,
    # HfHubModelNotFoundError,
    # HfHubModelDeletedError,
    # HfHubModelDisabledError,
    # HfHubModelPermissionError,
    # HfHubRateLimitExceededError,
)
from huggingface_hub import InferenceClient, HfApi
from huggingface_hub.errors import HfHubHTTPError, HFValidationError
import logging
logger = logging.getLogger(__name__)

class ModelServiceExceptionHandler:
    @staticmethod
    def handle_exception(e: Exception) -> str:
        if isinstance(e, HFValidationError):
            return "Invalid Hugging Face token. Please provide a valid token."
        # elif isinstance(e, (HfHubModelNotFoundError, HfHubModelDeletedError, HfHubModelDisabledError, HfHubModelPermissionError)):
        #     return "There is an issue with the selected model or provider. Please try choosing another model."
        # elif isinstance(e, HfHubRateLimitExceededError):
        #     return "Rate limit exceeded. Please try again after some time or choose a different model."
        elif isinstance(e, HfHubHTTPError):
            return "There was a problem connecting to Hugging Face. Please check your inputs or try again later."
        else:
            return "An unknown error occurred while generating the response. Please try again later or choose a different model."

class ModelService(ModelServiceExceptionHandler):
    def __init__(self, hf_token: str):
        self.client = InferenceClient(
            api_key=hf_token,
        )

    def generate_text(self, prompt: str, model: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )
            return completion.choices[0].message['content']
        except Exception as e:
            logger.error(f"Error in generate_text from hugging face: {e}", exc_info=True)
            # Use the handler to get a user-friendly message
            raise RuntimeError(self.handle_exception(e))
    
    def list_served_models(self) -> list:
        try:
            api = HfApi() 
            served_models = api.list_models(inference="warm", limit=200)
            return [model.modelId for model in served_models]
        except Exception as e:
            logger.error(f"Error in list_served_models from hugging face: {e}", exc_info=True)
            # Use the handler to get a user-friendly message
            raise RuntimeError(self.handle_exception(e))