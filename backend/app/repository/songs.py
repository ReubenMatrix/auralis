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
        duration: float,
        file_path: str,
        status: str
    ) -> int:

        query = text("""
                    SELECT add_song(:title, :artist, :album, :duration, :file_path, :status)
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
                        "file_path": file_path,
                        "status": status
                    }
                )
                conn.commit()
                song_id = result.scalar()

                logger.info(f"Soong Inserted With ID: {song_id}")
                return song_id

        except SQLAlchemyError as e:
            logger.error(f"Error In Adding New Song: {e}")
            raise

    @staticmethod
    def update_song(
        song_id: int,
        title: str | None = None,
        artist: str | None = None,
        album: str | None = None,
        duration: float | None = None,
        file_path: str | None = None,
        status: str | None = None
    ) -> bool:

        query = text("""
                    SELECT update_song(:song_id, :title, :artist, :album, :duration, :file_path, :status)
                     """)

        try:
            with get_db_connection() as conn:
                result = conn.execute(
                    query,
                    {
                        "song_id": song_id,
                        "title": title,
                        "artist": artist,
                        "album": album,
                        "duration": duration,
                        "file_path": file_path,
                        "status": status
                    }
                )
                conn.commit()
                logger.info(f"Song Updated Successfully")
                return result.scalar()

        except SQLAlchemyError as e:
            logger.error(f"Error In Updating Song: {e}")
            raise
