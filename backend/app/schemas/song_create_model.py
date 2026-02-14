from pydantic import BaseModel

class SongCreate(BaseModel):
    title: str
    artist: str
    album: str
    duration: float
    file_path: str