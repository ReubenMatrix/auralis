from sqlalchemy import text
from app.repository.db import get_db_connection
from app.core.logger import logger
from sqlalchemy.exc import SQLAlchemyError

class SongRepository:

    @staticmethod
    def add_song(
        title: str,
        artist: str,
        album: str,
        duration: str,
        file_path: str,
    ) -> int :
        
        query = text("""
                    SELECT add_song(:title, :artist, :album, :duration, :file_path)
                     """) 
        
        try:
            with get_db_connection() as conn:
                result = conn.execute(
                    query,
                    {
                        "title": title,
                        "artist": artist,
                        "album": album,
                        "duration": duration,
                        "file_path": file_path
                    }
                )
                conn.commit() 
                song_id = result.scalar()

                logger.info(f"Soong Inserted With ID: {song_id}")
                return song_id
        
        
        except SQLAlchemyError as e:
            logger.error(f"Error In Adding New Song: {e}")
            raise