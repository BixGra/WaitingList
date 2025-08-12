from fastapi import APIRouter
from fastapi.params import Depends

from app.managers import user_manager
from app.managers.postgres_manager import PostgresManager
from app.schemas.user_router_schemas import (
    GetAllStatusInput,
    GetAllStatusOutput,
    GetStatusInput,
    GetStatusOutput,
    JoinListInput,
    LeaveListInput,
)
from app.utils.dependencies import (
    get_postgres_manager,
)

router = APIRouter(tags=["User"], prefix="/user")


@router.post("/join-list")
async def join_list(
        join_list_input: JoinListInput,
        postgres_manager: PostgresManager = Depends(get_postgres_manager),
) -> GetStatusOutput:
    get_status_output = user_manager.join_list(
        join_list_input=join_list_input,
        postgres_manager=postgres_manager,
    )
    return get_status_output


@router.put("/leave-list")
async def leave_list(
        leave_list_input: LeaveListInput,
        postgres_manager: PostgresManager = Depends(get_postgres_manager),
) -> str:
    # TODO reason : tickets bought or simply leaving
    user_manager.leave_list(
        leave_list_input=leave_list_input,
        postgres_manager=postgres_manager,
    )
    # TODO Better success output
    return "success"


@router.get("/get-all-status")
async def get_all_status(
        user_id: str,
        postgres_manager: PostgresManager = Depends(get_postgres_manager),
) -> GetAllStatusOutput:
    data = {
        "user_id": user_id,
    }
    get_all_status_input = GetAllStatusInput(**data)
    get_all_status_output = user_manager.get_all_status(
        get_all_status_input=get_all_status_input,
        postgres_manager=postgres_manager,
    )
    return get_all_status_output


@router.get("/get-status")
async def get_status(
        user_id: str,
        offer_id: str,
        representation_id: str,
        postgres_manager: PostgresManager = Depends(get_postgres_manager),
) -> GetStatusOutput:
    data = {
        "user_id": user_id,
        "offer_id": offer_id,
        "representation_id": representation_id,
    }
    get_status_input = GetStatusInput(**data)
    get_status_output = user_manager.get_status(
        get_status_input=get_status_input,
        postgres_manager=postgres_manager,
    )
    return get_status_output
