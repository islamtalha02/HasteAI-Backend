# app/main.py
from .routes import router as main_router  # Adjusted import path
import uvicorn
from fastapi import FastAPI

app = FastAPI()

app.include_router(main_router)  # Using the imported router object

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)