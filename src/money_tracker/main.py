from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from money_tracker.core.config import get_settings
from money_tracker.infrastructure.postgres import engine

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Check DB Connection
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            print("✅ Database connection established successfully.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise e
    
    yield
    
    # Shutdown: Close DB Connection
    await engine.dispose()
    print("🛑 Database connection closed.")

from money_tracker.adapters.api.rest import auth

from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from money_tracker.adapters.api.limiter import limiter

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Register Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Money Tracker API is running", "db": "PostgreSQL connected"}
