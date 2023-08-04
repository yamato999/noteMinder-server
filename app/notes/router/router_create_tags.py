from typing import Any
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


class CreateTagsRequest(AppModel):
    description: str


class CreateTagsResponse(AppModel):
    id: Any = Field(alias="_id")
    title: str


@router.post("/values/", response_model=CreateTagsResponse)
def create_tags(
    input: CreateTagsRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    inserted_id = svc.repository.create_tags(user_id=user_id, payload=input.dict())
    return CreateTagsResponse(id=inserted_id)
