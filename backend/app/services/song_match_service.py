import tempfile
import shutil
from collections import defaultdict

from app.services.fingerprint_service import FingerprintService
from app.repository.song_match import SongMatchRepository


class SongMatchService:

    @staticmethod
    def match_song(audio_file):

        # 1️⃣ Save uploaded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            audio_file.file.seek(0)
            shutil.copyfileobj(audio_file.file, temp)
            temp_path = temp.name

        # 2️⃣ Generate QUERY fingerprints
        query_fingerprints = FingerprintService.generate_query_fingerprints(temp_path)

        if not query_fingerprints:
            return None

        # 3️⃣ Extract hashes
        hashes = list({h for h, _ in query_fingerprints})

        # 4️⃣ Fetch matched fingerprints from DB
        db_rows = SongMatchRepository.find_matched_song(hashes)

        if not db_rows:
            return None

        # 5️⃣ Offset-delta voting
        votes = defaultdict(int)
        query_map = defaultdict(list)

        for h, qt in query_fingerprints:
            query_map[h].append(qt)

        for row in db_rows:
            for qt in query_map[row.hash]:
                delta = round(row.time_offset - qt, 2)
                votes[(row.song_id, delta)] += 1

        if not votes:
            return None

        # 6️⃣ Best song
        (best_song_id, _), confidence = max(
            votes.items(),
            key=lambda x: x[1]
        )

        # 7️⃣ Fetch song metadata
        song = SongMatchRepository.get_song_by_id(best_song_id)

        if not song:
            return None

        return {
            "song_id": song.id,
            "title": song.title,
            "artist": song.artist,
            "album": song.album,
            "duration": song.duration,
            "file_path": song.file_path,
            "status": song.status,
            "confidence": confidence
        }