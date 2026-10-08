from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.ollama_service import ollama_service
from app.services.tts_service import tts_service
import json

router = APIRouter()

@router.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    # 1. Aceptar la conexión entrante desde el cliente (Flutter)
    await websocket.accept()
    print("Cliente WebSocket conectado.")

    try:
        while True:
            # 2. Escuchar mensajes del cliente en formato JSON
            data_raw = await websocket.receive_text()
            data = json.loads(data_raw)
            
            event_type = data.get("event")
            user_prompt = data.get("payload", "").strip()

            # 3. Procesar cuando el evento sea un texto enviado por el niño
            if event_type == "user_text" and user_prompt:
                
                # A) Avisar al cliente que la IA comenzó a procesar/responder
                await websocket.send_json({
                    "event": "start",
                    "content": ""
                })

                # B) Recorrer el generador asíncrono de Ollama y mandar palabra por palabra
                respuesta_acumulada = ""
                async for chunk in ollama_service.generar_respuesta_stream(user_prompt):
                    respuesta_acumulada += chunk
                    await websocket.send_json({
                        "event": "chunk",
                        "content": chunk
                    })

                audio_url = tts_service.sintetizar_audio(respuesta_acumulada)

                # C) Avisar al cliente que la respuesta finalizó
                await websocket.send_json({
                    "event": "end",
                    "content": ""
                })

    except WebSocketDisconnect:
        print("Cliente WebSocket desconectado.")
    except Exception as e:
        print(f"⚠️ Error en WebSocket: {e}")
        try:
            await websocket.send_json({
                "event": "error",
                "content": f"Ocurrió un error en el servidor: {str(e)}"
            })
        except:
            pass