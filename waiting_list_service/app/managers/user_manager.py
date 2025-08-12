from app.managers.postgres_manager import PostgresManager
from app.schemas.user_router_schemas import (
    GetAllStatusInput,
    GetAllStatusOutput,
    GetStatusInput,
    GetStatusOutput,
    JoinListInput,
    LeaveListInput,
)


def join_list(
        join_list_input: JoinListInput,
        postgres_manager: PostgresManager
) -> GetStatusOutput:
    postgres_manager.join_list(
        user_id=join_list_input.user_id,
        offer_id=join_list_input.offer_id,
        representation_id=join_list_input.representation_id,
        tickets_wanted=join_list_input.tickets_wanted,
    )
    update_status(
        offer_id=join_list_input.offer_id,
        representation_id=join_list_input.representation_id,
        postgres_manager=postgres_manager,
    )
    waiting_list_position, status, tickets_wanted = postgres_manager.get_status(
        user_id=join_list_input.user_id,
        offer_id=join_list_input.offer_id,
        representation_id=join_list_input.representation_id,
    )
    data = {
        "user_id": join_list_input.user_id,
        "offer_id": join_list_input.offer_id,
        "representation_id": join_list_input.representation_id,
        "status": status,
        "waiting_list_position": waiting_list_position,
        "tickets_wanted": tickets_wanted,
    }
    return GetStatusOutput(**data)


def leave_list(
        leave_list_input: LeaveListInput,
        postgres_manager: PostgresManager
) -> None:
    postgres_manager.leave_list(
        leave_list_input.user_id,
        leave_list_input.offer_id,
        leave_list_input.representation_id,
    )
    update_status(
        offer_id=leave_list_input.offer_id,
        representation_id=leave_list_input.representation_id,
        postgres_manager=postgres_manager,
    )


def get_all_status(
        get_all_status_input: GetAllStatusInput,
        postgres_manager: PostgresManager,
) -> GetAllStatusOutput:
    status_list = postgres_manager.get_all_status(
        user_id=get_all_status_input.user_id,
    )
    get_status_output_list = []
    for status_item in status_list:
        data = {
            "user_id": get_all_status_input.user_id,
            "offer_id": status_item.get("offer_id", ""),
            "representation_id": status_item.get("representation_id", ""),
        }
        get_status_input = GetStatusInput(**data)
        get_status_output_item = get_status(
            get_status_input=get_status_input,
            postgres_manager=postgres_manager,
        )
        get_status_output_list.append(get_status_output_item)
    get_all_status_output = GetAllStatusOutput(items=get_status_output_list)
    return get_all_status_output


def get_status(
        get_status_input: GetStatusInput,
        postgres_manager: PostgresManager,
) -> GetStatusOutput:
    waiting_list_position, status, tickets_wanted = postgres_manager.get_status(
        user_id=get_status_input.user_id,
        offer_id=get_status_input.offer_id,
        representation_id=get_status_input.representation_id,
    )
    data = {
        "user_id": get_status_input.user_id,
        "offer_id": get_status_input.offer_id,
        "representation_id": get_status_input.representation_id,
        "status": status,
        "waiting_list_position": waiting_list_position,
        "tickets_wanted": tickets_wanted,
    }
    return GetStatusOutput(**data)


def update_status(
        offer_id: str,
        representation_id: str,
        postgres_manager: PostgresManager,
) -> None:
    available_stock = postgres_manager.get_available_stock(
        offer_id=offer_id,
        representation_id=representation_id,
    )
    user_ids = postgres_manager.get_eligible_users(
        offer_id=offer_id,
        representation_id=representation_id,
        available_stock=available_stock,
    )
    for user_id in user_ids:
        send_notification(
            user_id=user_id,
            offer_id=offer_id,
            representation_id=representation_id,
        )


def send_notification(
        user_id: str,
        offer_id: str,
        representation_id: str,
) -> None:
    print(f"{user_id} - {offer_id} - {representation_id}")
