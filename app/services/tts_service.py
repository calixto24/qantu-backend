import os
import uuid
import wave
from piper import PiperVoice
from app.config import settings

class TTSService:
    def __init__(self):
        self.model_path = os.path.join("models", "tts", "es_ES-sharvard-medium.onnx")
        self.config_path = f"{self.model_path}.json"
        
        # 1. Asegurar que la carpeta de destino exista antes de intentar escribir
        os.makedirs(settings.TEMP_AUDIO_DIR, exist_ok=True)

        self.voice = None

        if os.path.exists(self.model_path) and os.path.exists(self.config_path):
            try:
                self.voice = PiperVoice.load(self.model_path, config_path=self.config_path)
                print("🔊 Modelo Piper TTS cargado correctamente en modo offline.")
            except Exception as e:
                print(f"⚠️ Error cargando Piper TTS: {e}")
        else:
            print(f"⚠️ No se encontraron los archivos del modelo en: {self.model_path}")

    def sintetizar_audio(self, texto: str) -> str:
        """Convierte texto en un archivo WAV usando Piper con logs detallados de error."""

        if not self.voice:
            print("❌ TTS: modelo no cargado.")
            return ""

        if not texto.strip():
            print("❌ TTS: texto vacío.")
            return ""

        filename = f"qantu_speech_{uuid.uuid4().hex[:8]}.wav"
        output_path = os.path.join(settings.TEMP_AUDIO_DIR, filename)

        try:
            print(f"🔊 TTS: sintetizando: {texto}")

            with wave.open(output_path, "wb") as wav_file:
                # Intentamos primero con la API clásica de Piper
                if hasattr(self.voice, "synthesize_wav"):
                    self.voice.synthesize_wav(texto.strip(), wav_file)
                else:
                    self.voice.synthesize(texto.strip(), wav_file)

            if os.path.exists(output_path):
                size = os.path.getsize(output_path)
                print(f"✅ TTS generado con éxito: {output_path} ({size} bytes)")
                return f"/audio/{filename}"

            print("❌ TTS: el archivo no fue creado.")
            return ""

        except Exception as e:
            print(f"❌ ERROR REAL DE PIPER TTS: {type(e).__name__}: {e}")

            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except Exception:
                    pass

            return ""

# Instancia singleton del servicio
tts_service = TTSService()