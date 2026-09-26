from fastapi import FastAPI
# from .database import Base, engine
from .routes import router
from .sync.routes import router as sync_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# Create all database tables (safe at import-time for simple apps)
# Base.metadata.create_all(bind=engine)

app = FastAPI( title="Nagarpanchayat API",
    version="1.0.0",)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000
)

app.get("/health")
async def health():
    return {
        "status": "ok"
    }


app.include_router(router)
app.include_router(sync_router)