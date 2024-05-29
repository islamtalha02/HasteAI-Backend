from fastapi import FastAPI, HTTPException
from app.routers.auth_router import router as auth_router
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from contextlib import asynccontextmanager


def create_tables():
    Base.metadata.create_all(engine)
    logging.info("Database Tables Created Successfully")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_tables()
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
    yield

app = FastAPI(lifespan=lifespan)
# Include the authentication router
app.include_router(auth_router)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    try:
        return {"message": "HAsteAI backend is running"}
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
