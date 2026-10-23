"""
Dashboard API для плагина jarvis-switch.
Эндпоинт: POST /api/plugins/jarvis-switch/switch
"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class SwitchRequest(BaseModel):
    target: str  # "visual" или "chat"


@router.post("/switch")
async def switch(req: SwitchRequest):
    """Переключает режим интерфейса."""
    target = req.target
    if target == "visual":
        return {"ok": True, "message": "Режим «Визуал» активирован"}
    elif target == "chat":
        return {"ok": True, "message": "Режим «Чат» активирован"}
    else:
        return {"ok": False, "message": f"Неизвестный режим: {target}"}
