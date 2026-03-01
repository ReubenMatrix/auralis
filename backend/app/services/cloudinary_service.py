import cloudinary
import cloudinary.uploader
from app.core.logger import logger
from app.core.config import settings

class CloudinaryService:

    @staticmethod
    def init_cloudinary():
        cloudinary.config(
            cloud_name = settings.CLOUDINARY_CLOUD_NAME,
            api_key = settings.CLOUDINARY_API_KEY,
            api_secret = settings.CLOUDINARY_SECRET_KEY
        )

    @staticmethod
    def upload_audio_file(file, song_id:int):
        try:
            result = cloudinary.uploader.upload(
                file,
                resource_type = "video",
                public_id=f"song_{song_id}",
                folder="shazam/audio"
            )

            logger.info(f"File Uploaded To Cloudinary : {result['secure_url']}")
            return result['secure_url']
        
        except Exception as e:
            logger.error(f"Cloudinary upload failed: {e}")
            raise
