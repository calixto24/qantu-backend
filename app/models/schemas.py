from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    pregunta: str

class ChatResponse(BaseModel):
    respuesta_texto: str
    status: str = "success"

class WSInputMessage(BaseModel):
    event: str     
    payload: str   

class WSOutputMessage(BaseModel):
    event: str     
    content: Optional[str] = None