import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.db.base import Base
from app.db.session import engine

# Route imports
from app.api.v1.health import router as health_router
from app.api.v1.providers import router as providers_router
from app.api.v1.sessions import router as sessions_router
from app.api.v1.messages import router as messages_router
from app.api.v1.artifacts import router as artifacts_router
from app.api.v1.ingest import router as ingest_router

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("application_startup", project=settings.PROJECT_NAME, version=settings.VERSION)
    # Ensure DB tables exist on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    logger.info("application_shutdown")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("unhandled_exception", path=request.url.path, error=str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please try again or check server logs."
            }
        }
    )


# Include Routers
app.include_router(health_router, tags=["Health"])
app.include_router(providers_router, prefix=settings.API_V1_STR, tags=["LLM Providers"])
app.include_router(sessions_router, prefix=settings.API_V1_STR, tags=["Sessions"])
app.include_router(messages_router, prefix=settings.API_V1_STR, tags=["Messages"])
app.include_router(artifacts_router, prefix=settings.API_V1_STR, tags=["Artifacts"])
app.include_router(ingest_router, prefix=settings.API_V1_STR, tags=["Ingestion"])


@app.get("/")
async def root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "status": "online"
    }
