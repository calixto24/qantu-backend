from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    pregunta: str

class ChatResponse(BaseModel):
    respuesta_texto: str
    status: str = "success"