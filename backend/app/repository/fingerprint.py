from sqlalchemy import text
from app.repository.db import get_db_connection
from app.core.logger import logger
from sqlalchemy.exc import SQLAlchemyError
from typing import Iterable
from app.schemas.song_fingerprint_model import FingerprintCreate


class FingerprintRepository:

    @staticmethod
    def save_many(fingerprints: Iterable[FingerprintCreate]):
        query = text("""
            SELECT add_fingerprint(:hash, :song_id, :time_offset)
        """)

        try:
            with get_db_connection() as conn:
                for fp in fingerprints:
                    conn.execute(
                        query,
                        {
                            "hash": fp.hash,
                            "song_id": fp.song_id,
                            "time_offset": fp.time_offset
                        }
                    )

                conn.commit()

            logger.info(
                f"Inserted {len(list(fingerprints))} fingerprints"
            )

        except SQLAlchemyError as e:
            logger.error(f"Error adding fingerprints: {e}")
            raise