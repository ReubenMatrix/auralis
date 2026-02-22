from app.repository.db import get_db_connection
from sqlalchemy import text

class SongMatchRepository:
    @staticmethod
    def find_matched_song(hashes):
        query = text("""
                    SELECT * FROM get_matched_fingerprints(:hashes)
                     """)
        
        with get_db_connection() as conn:
            result = conn.execute(
                query,
                {
                    "hashes": hashes
                }
            )
            rows = result.fetchall()

        return rows
    
    @staticmethod
    def get_song_by_id(song_id):
        query = text("""
            SELECT * FROM get_song_by_id(:song_id)
        """)

        with get_db_connection() as conn:
            result = conn.execute(query, {"song_id": song_id})
            return result.fetchone()
