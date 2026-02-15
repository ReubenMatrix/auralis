from pydantic import BaseModel
from typing import Optional

class SongCreate(BaseModel):
    title: str
    artist: str
    album: str
    duration: float
    file_path: str
    status: str



class SongUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    duration: Optional[float] = None
    file_path: Optional[str] = None
    status: Optional[str] = None