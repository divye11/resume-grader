from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os


load_dotenv()

app = FastAPI()
origins = [
   "http://localhost",
   "http://localhost:3000",
]

app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=[""],
   allow_headers=[""],
)

MONGODB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.resume_grader

app.state.db = db

from jobs.router import router as JobRoutes
from candidates.router import router as CandidateRoutes
from grading.router import router as GradingRoutes
app.include_router(JobRoutes)
app.include_router(CandidateRoutes)
app.include_router(GradingRoutes)

@app.get("/")
def hello_world():
    return {"message": "Resume grader is working"}

def start():
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()