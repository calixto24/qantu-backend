from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.schemas import ChatRequest, ChatResponse
from app.services.ollama_service import ollama_service
from app.services.stt_service import stt_service 
from app.config import settings
import shutil
import os
import uuid

router = APIRouter()

@router.post("/chat/texto", response_model=ChatResponse)
async def chat_texto(request: ChatRequest):
    if not request.pregunta.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")
    
    respuesta_chunks = []
    async for chunk in ollama_service.generar_respuesta_stream(request.pregunta):
        respuesta_chunks.append(chunk)
        
    respuesta_completa = "".join(respuesta_chunks)
    
    return ChatResponse(
        respuesta_texto=respuesta_completa
    )

@router.post("/stt/transcribir")
async def transcribir_audio(file: UploadFile = File(...)):
    """Recibe el audio grabado en Flutter Web, lo transcribe con Whisper y retorna solo el texto."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Archivo de audio no válido.")

    # Guardar archivo temporalmente
    file_extension = os.path.splitext(file.filename)[1] or ".wav"
    temp_filename = f"stt_{uuid.uuid4().hex[:8]}{file_extension}"
    temp_path = os.path.join(settings.TEMP_AUDIO_DIR, temp_filename)

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Transcribir con el modelo local de Whisper
        texto_transcrito = stt_service.transcribir_audio(temp_path)

        if not texto_transcrito:
            raise HTTPException(status_code=400, detail="No se logró entender el audio grabado.")

        return {
            "status": "success",
            "texto": texto_transcrito
        }

    finally:
        # Limpieza del archivo temporal
        if os.path.exists(temp_path):
            os.remove(temp_path)