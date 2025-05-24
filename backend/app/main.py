# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your router
from .routers import occupancy

app = FastAPI(
    title="AI Occupancy Planning System",
    description="Natural Language Interface for Workspace Allocation",
    version="0.1.0",
)

# CORS configuration
origins = [
    "http://localhost:3000",  # Your Next.js frontend
    # Add other frontend origins if deployed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API router
app.include_router(occupancy.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Occupancy Planning System API!"}