from faster_whisper import WhisperModel
import os

class STTService:
    def __init__(self):
        self.model_size = "base"
        self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")

    def transcribir_audio(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe.")

        try:
            segments, _ = self.model.transcribe(
                file_path, 
                language="es",
                beam_size=5
            )
            
            texto_transcrito = "".join([segment.text for segment in segments])
            return texto_transcrito.strip()
            
        except Exception as e:
            print(f"Error procesando el audio en Whisper: {e}")
            return ""

stt_service = STTService()