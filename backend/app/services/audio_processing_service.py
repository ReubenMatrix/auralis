import librosa
import numpy as np
from scipy.ndimage import maximum_filter


class AudioProcessingService:
    SAMPLE_RATE = 22050
    N_FFT = 4096
    HOP_LENGTH = 512
    PEAK_NEIGHBORHOOD_SIZE = 200

    @staticmethod
    def extract_peaks(audio_path: str):
        y, sr = librosa.load(audio_path, sr = AudioProcessingService.SAMPLE_RATE, mono=True)

        spectogram = np.abs(
            librosa.stft(y, n_fft=AudioProcessingService.N_FFT, hop_length=AudioProcessingService.HOP_LENGTH)
        )

        spectogram_db = librosa.amplitude_to_db(spectogram, ref=np.max)

        neighborhood = maximum_filter(
            spectogram_db,
            size=AudioProcessingService.PEAK_NEIGHBORHOOD_SIZE
        )

        peaks = (spectogram_db == neighborhood) & (spectogram_db > -30)

        return np.argwhere(peaks), sr