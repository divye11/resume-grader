from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

#Routes
from jobs.router import router as JobRoutes

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

app.include_router(JobRoutes)

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

def start():
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()