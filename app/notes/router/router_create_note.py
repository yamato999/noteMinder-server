from typing import Any
from ..adapters.gpt_service import generate_title
from fastapi import Depends
from pydantic import Field
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Обработчик для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class CreateNoteRequest(AppModel):
    description: str


class CreateNoteResponse(AppModel):
    id: Any = Field(alias="_id")
    title: str


@router.post("/", response_model=CreateNoteResponse)
def create_note(
    input: CreateNoteRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    
    title = generate_title(input.description)
    logger.debug(f"Value of variable: {title}")
    user_id = jwt_data.user_id
    inserted_id = svc.repository.create_note(user_id=user_id, payload=input.dict(), title=title)
    return CreateNoteResponse(id=inserted_id, title=title)
