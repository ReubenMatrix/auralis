from fastapi import APIRouter, HTTPException, status
from app.schemas.song_create_model import SongCreate
from app.core.logger import logger
from app.repository.songs import SongRepository

router = APIRouter(
    prefix = '/songs',
    tags=["Songs"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_song(song: SongCreate):
    try:
        song_id = SongRepository.add_song(
            title=song.title,
            artist=song.artist,
            album= song.album,
            duration=song.duration,
            file_path=song.file_path
        )

        return{
            "message": "Song Added Succesfully",
            "song_id": song_id
        }

    except Exception as e:
        logger.error(f"Failed To Create Song: {e}")
        raise HTTPException(
            status_code = 400,
            detail=str(e)
        )