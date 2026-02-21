from pydantic import BaseModel

class FingerprintCreate(BaseModel):
    hash: str
    song_id: int
    time_offset: float