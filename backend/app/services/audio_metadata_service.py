import librosa
import tempfile
import os
from fastapi import UploadFile
from app.core.logger import logger

class AudioMetadataService:
    @staticmethod
    def get_duration(file: UploadFile) -> float:
        try:
            suffix = os.path.splitext(file.filename)[-1] or ".tmp"

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file.file.read())
                tmp_path = tmp.name

            try:
                y, sr = librosa.load(tmp_path, sr=None)
                duration = librosa.get_duration(y=y, sr=sr)
                logger.info("Calculated Duration")
                return duration
            finally:
                os.unlink(tmp_path)

        except Exception as e:
            logger.error(f"Error Occured While Calculating Duration: {e}")
            raise


    @staticmethod
    def get_updated_duration(file_obj, filename: str) -> float:
        try:
            suffix = os.path.splitext(filename)[-1] or ".tmp"

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file_obj.read())
                tmp_path = tmp.name

            try:
                y, sr = librosa.load(tmp_path, sr=None)
                duration = librosa.get_duration(y=y, sr=sr)
                logger.info("Calculated Duration")
                return duration
            finally:
                os.unlink(tmp_path)

        except Exception as e:
            logger.error(f"Error Occured While Calculating Duration: {e}")
            raise