from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI(title="RAG Service API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

from .api import app as api_app

for route in api_app.routes:
    app.routes.append(route)

@app.get("/", include_in_schema=False)
async def root():
    """
    Redirect to API documentation.
    """
    return RedirectResponse(url="/docs")

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
