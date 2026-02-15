from fastapi import APIRouter, HTTPException, status
from app.schemas.song_create_model import SongCreate, SongUpdate
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
            album=song.album,
            duration=song.duration,
            file_path=song.file_path,
            status=song.status,
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
    

@router.patch("/{song_id}", status_code = status.HTTP_200_OK)
def update_song(song_id: int, song: SongUpdate):
    try:
        updated = SongRepository.update_song(
            song_id=song_id,
            title=song.title,
            artist=song.artist,
            album=song.album,
            duration=song.duration,
            file_path=song.file_path,
            status=song.status
        ),

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Song not found"
            )

        return {
            "message": "Song updated successfully",
            "song_id": song_id
        }

    except Exception as e:
        logger.error(f"Failed to update song {song_id}: {e}")
        raise HTTPException(
            status_code = 400,
            detail=str(e)
        )