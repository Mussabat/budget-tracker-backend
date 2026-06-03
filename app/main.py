from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models.models import Base
from app.routers import categories, subcategories, transactions

app = FastAPI(
    title="Budget Tracker API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(categories.router)
app.include_router(subcategories.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return {"message": "Budget Tracker API is running"}