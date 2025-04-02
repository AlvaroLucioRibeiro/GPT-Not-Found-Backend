import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.modules_api import router

# Initialize the FastAPI application
app = FastAPI()

#Enable CORS for all origins
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(router)

if __name__ == "__main__":
    # Run the application with Uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
