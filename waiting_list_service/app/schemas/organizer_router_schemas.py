from datetime import datetime

from pydantic import BaseModel, field_validator

from app.schemas.user_router_schemas import GetStatusOutput
from app.utils.errors import (
    NegativeAddStockError,
    NegativeRemoveStockError,
)
from app.utils.tools import Status

class AddStockInput(BaseModel):
    offer_id: str
    representation_id: str
    stock_amount: int

    @field_validator('stock_amount')
    def tickets_wanted_non_null(cls, v):
        if v > 0:
            return v
        else:
            raise NegativeAddStockError


class RemoveStockInput(BaseModel):
    offer_id: str
    representation_id: str
    stock_amount: int

    @field_validator('stock_amount')
    def tickets_wanted_non_null(cls, v):
        if v > 0:
            return v
        else:
            raise NegativeRemoveStockError


class BuyTicketsInput(BaseModel):
    user_id: str
    offer_id: str
    representation_id: str


class GetWaitingListsInput(BaseModel):
    user_ids: list[str] = []
    offer_ids: list[str] = []
    representation_ids: list[str] = []
    event_ids: list[str] = []
    status: list[Status] = []


class WaitingListsItem(BaseModel):
    user_id: str
    created_at: datetime
    tickets_wanted: int
    status: Status


class WaitingListsOffRep(BaseModel):
    items: list[WaitingListsItem]
    offer_id: str
    representation_id: str


class WaitingListsEvent(BaseModel):
    items: list[WaitingListsOffRep]
    event_id: str


class GetWaitingListsOutput(BaseModel):
    waiting_lists: list[WaitingListsEvent]
