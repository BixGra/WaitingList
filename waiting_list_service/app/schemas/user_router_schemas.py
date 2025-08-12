from pydantic import BaseModel, field_validator

from app.utils.errors import MinimumWantedTicketsError
from app.utils.tools import Status


class JoinListInput(BaseModel):
    user_id: str
    offer_id: str
    representation_id: str
    tickets_wanted: int

    @field_validator('tickets_wanted')
    def tickets_wanted_non_null(cls, v):
        if v > 0:
            return v
        else:
            raise MinimumWantedTicketsError


class LeaveListInput(BaseModel):
    user_id: str
    offer_id: str
    representation_id: str


class GetStatusInput(BaseModel):
    user_id: str
    offer_id: str
    representation_id: str


class GetStatusOutput(BaseModel):
    user_id: str
    offer_id: str
    representation_id: str
    status: Status
    tickets_wanted: int


class GetAllStatusInput(BaseModel):
    user_id: str


class GetAllStatusOutput(BaseModel):
    items: list[GetStatusOutput]
