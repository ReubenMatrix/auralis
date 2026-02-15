import librosa
from app.core.logger import logger

class AudioMetadataService:
    @staticmethod
    def get_duration(file) -> float:
        try:
            y, sr = librosa.load(file.file, sr=None)
            duration = librosa.get_duration(y=y, sr=sr)
            logger.info("Calculated Duration")
            return duration
        
        except Exception as e:
            logger.error(f"Error Occured While Calculating Duration: {e}")
            raise