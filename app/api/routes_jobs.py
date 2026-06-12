from datetime import datetime
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Track
from app.schemas import InstrumentalRequest, TrackResponse
from app.services.music_service import MusicService

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/health")
def health_check():
    return {"success": True, "status": "ok", "service": "jobs"}


@router.post("/generate-instrumental", response_model=TrackResponse)
def generate_instrumental(data: InstrumentalRequest):
    service = MusicService()

    try:
        result = service.generate_instrumental(
            prompt=data.prompt,
            duration=data.duration
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    db: Session = SessionLocal()
    try:
        track = Track(
            prompt=result["prompt"],
            title="ACE-Step Track",
            provider=result["provider"],
            audio_path=result["audio_path"],
            duration=result["duration"],
            created_at=datetime.now().isoformat()
        )
        db.add(track)
        db.commit()
        db.refresh(track)
        return track
    finally:
        db.close()


@router.get("/tracks", response_model=list[TrackResponse])
def get_tracks():
    db: Session = SessionLocal()
    try:
        return db.query(Track).order_by(Track.id.desc()).all()
    finally:
        db.close()