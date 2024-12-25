from fastapi import FastAPI
from app.routers import example

app = FastAPI()

app.include_router(example.router, prefix="/api/v1", tags=["examples"])

@app.get("/")
def root():
    return {"message": "Fast API Is Running"}