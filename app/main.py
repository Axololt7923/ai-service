from fastapi import FastAPI
from app.routers import cv, recommend

app = FastAPI(
    title="CareerMatch AI Service",
    version="1.0.0",
    description="AI service for CV parsing and job recommendation"
)


app.include_router(cv.router)


app.include_router(recommend.router)


@app.get("/health")
def health():
    return {"status": "ok"}