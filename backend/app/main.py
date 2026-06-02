from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.circular_route import router as circular_route_router

app = FastAPI(title="fun-nav API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(circular_route_router)


@app.get("/health")
def health():
    return {"status": "ok"}
