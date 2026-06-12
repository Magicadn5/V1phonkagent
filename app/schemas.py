from pydantic import BaseModel


class InstrumentalRequest(BaseModel):
    prompt: str
    duration: int = 60


class TrackResponse(BaseModel):
    id: int
    prompt: str
    title: str | None = None
    provider: str
    audio_path: str
    duration: float | None = None
    created_at: str | None = None

    class Config:
        from_attributes = True