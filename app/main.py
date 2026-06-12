from fastapi import FastAPI
from app.database import Base, engine
from app.api.routes_jobs import router as jobs_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Phonk Agent API V3")

@app.get("/")
def root():
    return {"message": "Phonk Agent API V3 running"}

app.include_router(jobs_router)