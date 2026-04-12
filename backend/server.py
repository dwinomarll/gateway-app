import asyncio, logging
from typing import Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Body
from fastapi.middleware.cors import CORSMiddleware
from backend.health import get_health
from backend.notion import get_my4_notes, get_page, update_page
from backend.chat import proxy_chat
from backend.config import HEALTH_POLL_INTERVAL

log = logging.getLogger("gateway.server")
app = FastAPI(title="GATEWAY Core", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
_connected: list[WebSocket] = []

async def broadcast(data: dict) -> None:
    dead = []
    for ws in _connected:
        try:
            await ws.send_json(data)
        except Exception:
            dead.append(ws)
    for ws in dead:
        _connected.remove(ws)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    _connected.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        if websocket in _connected:
            _connected.remove(websocket)

async def _health_poll_loop() -> None:
    while True:
        await asyncio.sleep(HEALTH_POLL_INTERVAL)
        status = await get_health()
        await broadcast({"type": "health", "data": status})

@app.on_event("startup")
async def startup() -> None:
    asyncio.create_task(_health_poll_loop())

@app.get("/health")
async def health_endpoint() -> dict:
    return await get_health()

@app.get("/notion")
async def notion_feed() -> list[dict[str, Any]]:
    return await get_my4_notes()

@app.get("/notion/{page_id}")
async def notion_page(page_id: str) -> dict[str, Any]:
    return await get_page(page_id)

@app.patch("/notion/{page_id}")
async def notion_update(page_id: str, properties: dict[str, Any] = Body(...)) -> dict[str, Any]:
    result = await update_page(page_id, properties)
    await broadcast({"type": "notion_update", "page_id": page_id, "data": result})
    return result

@app.post("/chat")
async def chat_endpoint(message: dict[str, Any]) -> dict[str, Any]:
    return await proxy_chat(message)
