from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.routes import router


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "AI-powered legal document generation API."
    ),
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=settings.allowed_origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "service": settings.app_name,
        "status": "ok",
        "version": settings.app_version,
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }