
import io
import os
from app.core.celery import celery_app
from app.core.logger import logger
from app.services.cloudinary_service import CloudinaryService
from app.repository.songs import SongRepository
from app.services.song_to_fingerprint_service import SongToFingerprintService
from app.services.audio_metadata_service import AudioMetadataService


@celery_app.task(bind=True, max_retries=3)
def process_audio_task(self, song_id: int, file_path: str):
    try:
        with open(file_path, "rb") as f:
            audio_bytes = f.read()

        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = os.path.basename(file_path)

        duration = AudioMetadataService.get_updated_duration(
            audio_file,
            audio_file.name
        )
        audio_file.seek(0)

        audio_url = CloudinaryService.upload_audio_file(audio_file, song_id)

        audio_file.seek(0)
        SongToFingerprintService.fingerprint_and_store(
            audio_file=audio_file,
            song_id=song_id
        )

        SongRepository.update_song(
            song_id=song_id,
            file_path=audio_url,
            duration=duration,
            status="COMPLETED"
        )

        os.remove(file_path)

    except Exception as e:
        logger.error(f"Task failed for song {song_id}: {e}")
        SongRepository.update_song(song_id=song_id, status="FAILED")

        raise self.retry(exc=e, countdown=2 ** self.request.retries)
