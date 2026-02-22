from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from app.schemas.song_create_model import SongCreate, SongUpdate
from app.core.logger import logger
from app.repository.songs import SongRepository
from app.repository.fingerprint import FingerprintRepository
from app.services.cloudinary_service import CloudinaryService
from app.services.audio_metadata_service import AudioMetadataService
from app.services.song_to_fingerprint_service import SongToFingerprintService
from app.services.song_match_service import SongMatchService

router = APIRouter(
    prefix='/songs',
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

        return {
            "message": "Song Added Succesfully",
            "song_id": song_id
        }

    except Exception as e:
        logger.error(f"Failed To Create Song: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_song(
    title: str = Form(...),
    artist: str = Form(...),
    album: str = Form(...),
    # duration: float = Form(...),
    audio: UploadFile = File(...)
):
    try:
        duration = AudioMetadataService.get_duration(audio) 
        song_id = SongRepository.add_song(
            title=title,
            artist=artist,
            album=album,
            duration=duration,
            file_path=None,
            status="PENDING"
        )

        try:
            audio.file.seek(0)
            audio_url = CloudinaryService.upload_audio_file(audio, song_id)

            SongRepository.update_song(
                song_id=song_id,
                file_path=audio_url,
                status="COMPLETED"
            )


            SongToFingerprintService.fingerprint_and_store(
                audio_file=audio.file,
                song_id=song_id
            )

        
 


            return {
                "message": "Song uploaded successfully",
                "song_id": song_id,
                "audio_url": audio_url
            }

        except Exception as upload_error:
            SongRepository.update_song(
                song_id=song_id,
                status="FAILED"
            )
            raise upload_error

    except Exception as e:
        logger.error(f"Failed To Create Song: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.patch("/{song_id}", status_code=status.HTTP_200_OK)
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
            status_code=400,
            detail=str(e)
        )



@router.post(
    "/match",
    status_code=status.HTTP_200_OK
)
def match_song(audio: UploadFile = File(...)):
    """
    Upload a short audio clip to identify the song
    """

    # Basic validation
    if not audio.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an audio file."
        )

    try:
        result = SongMatchService.match_song(audio)

        if not result:
            return {
                "matched": False,
                "message": "No matching song found"
            }

        return {
            "matched": True,
            "song": result
        }

    except Exception as e:
        logger.error(f"Song match failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Song matching failed"
        )