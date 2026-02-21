import tempfile
import shutil
from app.services.fingerprint_service import FingerprintService
from app.repository.fingerprint import FingerprintRepository


class SongToFingerprintService:

    @staticmethod
    def fingerprint_and_store(audio_file, song_id: int):
        # Save uploaded file temporarily
        audio_file.seek(0)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            shutil.copyfileobj(audio_file, temp)
            temp_path = temp.name

        # Generate fingerprints
        fingerprints = FingerprintService.generate_fingerprints(
            audio_path=temp_path,
            song_id=song_id
        )

        # Store fingerprints
        FingerprintRepository.save_many(fingerprints)