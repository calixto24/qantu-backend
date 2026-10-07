import httpx
import json
from app.config import settings

class OllamaService:
    def __init__(self):
        self.url = f"{settings.OLLAMA_BASE_URL}/api/generate"

    async def generar_respuesta_stream(self, prompt: str):
        """Envia la consulta a Ollama y retorna los tokens en streaming."""
        
        full_prompt = (
            f"{settings.SYSTEM_PROMPT}\n\n"
            f"Pregunta del niño: {prompt}\n"
            f"Qantu:"
        )
        
        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": full_prompt,
            "stream": True
        }

        # Usamos httpx.AsyncClient para llamadas HTTP asíncronas
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                async with client.stream("POST", self.url, json=payload) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line:
                            data = json.loads(line)
                            chunk = data.get("response", "")
                            yield chunk
            except Exception as e:
                yield f"[Error al conectar con Ollama: {str(e)}]"

ollama_service = OllamaService()