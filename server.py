import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api.forecasting import router as forecasting_router

# Load env variables from .env
load_dotenv()

app = FastAPI(
    title="Sintesa ANN Forecasting API",
    description="FastAPI microservice for predicting Inflation, CPI (IHK), and Commodities using Artificial Neural Networks.",
    version="1.0.0"
)

# Enable CORS for frontend and other services
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(forecasting_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Sintesa ANN Forecasting API",
        "endpoints": {
            "root": "/",
            "forecast": "/api/forecast [POST]"
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    # Run server
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
