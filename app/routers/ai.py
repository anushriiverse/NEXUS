from fastapi import APIRouter
from pydantic import BaseModel
from app.services.gemini_service import interpret_intent

router = APIRouter()


class IntentRequest(BaseModel):
    message: str


@router.post("/intent")
def get_intent(req: IntentRequest):
    return interpret_intent(req.message)
