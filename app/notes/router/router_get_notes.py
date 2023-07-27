from typing import Any, List

from fastapi import Depends, Response
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GetNoteResponse(AppModel):
    id: Any = Field(alias="_id")
    title: str
    description: str
    user_id: Any


@router.get("/all", response_model=List[GetNoteResponse])
def get_all_notes(
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service)
) -> List[GetNoteResponse]:
    notes = svc.repository.get_all_notes(user_id=jwt_data.user_id)
    return [GetNoteResponse(**note) for note in notes]
