from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import json

from app.database import SessionLocal
from app.models import Track

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/suno")
async def suno_callback(request: Request):
    raw_body = await request.body()
    print("RAW BODY:", raw_body)

    try:
        payload = json.loads(raw_body)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": f"Invalid JSON body: {str(e)}",
                "raw_body": raw_body.decode("utf-8", errors="ignore")
            }
        )

    db: Session = SessionLocal()

    try:
        data_block = payload.get("data", {})
        callback_type = data_block.get("callbackType")
        task_id = data_block.get("task_id")
        tracks = data_block.get("data", [])

        for item in tracks:
            track_uid = item.get("id")
            if not track_uid or not task_id:
                continue

            existing = db.query(Track).filter(Track.track_uid == track_uid).first()

            if existing:
                existing.task_id = task_id
                existing.callback_type = callback_type
                existing.title = item.get("title")
                existing.tags = item.get("tags")
                existing.prompt = item.get("prompt")
                existing.model_name = item.get("model_name")
                existing.audio_url = item.get("audio_url")
                existing.source_audio_url = item.get("source_audio_url")
                existing.stream_audio_url = item.get("stream_audio_url")
                existing.image_url = item.get("image_url")
                existing.source_image_url = item.get("source_image_url")
                existing.duration = item.get("duration")
                existing.create_time = str(item.get("createTime")) if item.get("createTime") else None
            else:
                new_track = Track(
                    task_id=task_id,
                    callback_type=callback_type,
                    track_uid=track_uid,
                    title=item.get("title"),
                    tags=item.get("tags"),
                    prompt=item.get("prompt"),
                    model_name=item.get("model_name"),
                    audio_url=item.get("audio_url"),
                    source_audio_url=item.get("source_audio_url"),
                    stream_audio_url=item.get("stream_audio_url"),
                    image_url=item.get("image_url"),
                    source_image_url=item.get("source_image_url"),
                    duration=item.get("duration"),
                    create_time=str(item.get("createTime")) if item.get("createTime") else None,
                )
                db.add(new_track)

        db.commit()
        return {"ok": True}

    finally:
        db.close()