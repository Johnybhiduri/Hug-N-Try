from fastapi import FastAPI
from app.routes import model_router

app = FastAPI()
app.include_router(model_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Hug-N-Try API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)