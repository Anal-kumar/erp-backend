import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Suppress annoying asyncio connection reset errors on Windows
logging.getLogger("asyncio").setLevel(logging.CRITICAL)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    swagger_ui_parameters={
        'defaultModelsExpanDepth': -1
    }
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to Rice Mill ERP API"}

@app.get(f"{settings.API_V1_STR}/health")
def health_check():
    return {"status": "healthy"}

from app.api.v1.api import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)