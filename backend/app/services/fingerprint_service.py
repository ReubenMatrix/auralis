import hashlib
from app.services.audio_processing_service import AudioProcessingService
from typing import List, Tuple
from app.schemas.song_fingerprint_model import FingerprintCreate


class FingerprintService:
    FAN_VALUE = 5 

    @staticmethod
    def generate_fingerprints(audio_path: str, song_id: int) -> List[FingerprintCreate]:
        peak_points, sr = AudioProcessingService.extract_peaks(audio_path)
        fingerprints = []

        for i in range(len(peak_points)):
            freq1, time1 = peak_points[i]

            for j in range(1, FingerprintService.FAN_VALUE):
                if i + j >= len(peak_points):
                    break

                freq2, time2 = peak_points[i + j]

                delta = time2 - time1


                if 0 < delta <= 200:
                    raw = f"{freq1}|||{freq2}|||{delta}"
                    hash_value = hashlib.md5(raw.encode()).hexdigest()

                    time_offset = time1 * AudioProcessingService.HOP_LENGTH / sr

                    fingerprints.append(FingerprintCreate(
                     hash=hash_value,
                     song_id = song_id,
                     time_offset = time_offset
                    ))  
        return fingerprints




