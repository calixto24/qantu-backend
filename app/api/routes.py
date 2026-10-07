from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.ollama_service import ollama_service

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