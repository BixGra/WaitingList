from itertools import groupby

from app.managers import user_manager
from app.managers.postgres_manager import PostgresManager
from app.schemas.organizer_router_schemas import (
    AddStockInput,
    BuyTicketsInput,
    GetWaitingListsInput,
    GetWaitingListsOutput,
    RemoveStockInput,
    WaitingListsEvent,
    WaitingListsItem,
    WaitingListsOffRep,
)
from app.utils.errors import (
    NotInWaitingListError,
    NotReadyError,
    RemoveStockValueError,
    UnknownStatusError,
)


def add_total_stock(
        add_total_stock_input: AddStockInput,
        postgres_manager: PostgresManager
) -> None:
    postgres_manager.add_total_stock(
        add_total_stock_input.offer_id,
        add_total_stock_input.representation_id,
        add_total_stock_input.stock_amount,
    )
    user_manager.update_status(
        offer_id=add_total_stock_input.offer_id,
        representation_id=add_total_stock_input.representation_id,
        postgres_manager=postgres_manager,
    )

def add_stock(
        add_stock_input: AddStockInput,
        postgres_manager: PostgresManager
) -> None:
    postgres_manager.add_stock(
        add_stock_input.offer_id,
        add_stock_input.representation_id,
        add_stock_input.stock_amount,
    )
    user_manager.update_status(
        offer_id=add_stock_input.offer_id,
        representation_id=add_stock_input.representation_id,
        postgres_manager=postgres_manager,
    )

def remove_stock(
        remove_stock_input: RemoveStockInput,
        postgres_manager: PostgresManager
) -> None:
    available_stock = postgres_manager.get_available_stock(
        remove_stock_input.offer_id,
        remove_stock_input.representation_id,
    )
    if remove_stock_input.stock_amount <= available_stock:
        postgres_manager.remove_stock(
            remove_stock_input.offer_id,
            remove_stock_input.representation_id,
            remove_stock_input.stock_amount,
        )
    # TODO If stock_amount = available_sock AND waiting list not open
    #   Open the waiting_list
    else:
        raise RemoveStockValueError


def buy_tickets(
        buy_tickets_input: BuyTicketsInput,
        postgres_manager: PostgresManager
) -> None:
    get_status_output = user_manager.get_status(
        get_status_input=buy_tickets_input,
        postgres_manager=postgres_manager,
    )
    match get_status_output.status:
        case "ready":
            # TODO should not occur due to the way users are set to ready
            #   but we can check if there are enough tickets available
            data = {
                "offer_id": buy_tickets_input.offer_id,
                "representation_id": buy_tickets_input.representation_id,
                "stock_amount": get_status_output.tickets_wanted
            }
            remove_stock_input = RemoveStockInput(**data)
            remove_stock(
                remove_stock_input=remove_stock_input,
                postgres_manager=postgres_manager,
            )
            user_manager.leave_list(
                leave_list_input=buy_tickets_input,
                postgres_manager=postgres_manager,
            )
        case "waiting":
            raise NotReadyError
        case "left":
            raise NotInWaitingListError
        case _:
            raise UnknownStatusError


def get_waiting_lists(
        get_waiting_lists_input=GetWaitingListsInput,
        postgres_manager=PostgresManager,
) -> GetWaitingListsOutput:
    waiting_lists = postgres_manager.get_waiting_lists(
        user_ids=get_waiting_lists_input.user_ids,
        offer_ids=get_waiting_lists_input.offer_ids,
        representation_ids=get_waiting_lists_input.representation_ids,
        event_ids=get_waiting_lists_input.event_ids,
        status=get_waiting_lists_input.status,
    )
    # Group by event
    waiting_lists_output = []
    for event_id, event_waiting_lists in groupby(waiting_lists, key=lambda x: (x.get("event_id", ""))):
        # Group by offer/representation
        waiting_lists_events = []
        for (offer_id, representation_id), waiting_list in groupby(event_waiting_lists, key=lambda x: (x.get("offer_id", ""), x.get("representation_id", ""))):
            items = list(sorted(list(map(lambda x: WaitingListsItem(**x), waiting_list)), key=lambda x: x.created_at))
            data = {
                "items": items,
                "offer_id": offer_id,
                "representation_id": representation_id,
            }
            waiting_lists_events.append(WaitingListsOffRep(**data))
        data = {
            "items": waiting_lists_events,
            "event_id": event_id,
        }
        waiting_lists_output.append(WaitingListsEvent(**data))
    data = {
        "waiting_lists": waiting_lists_output,
    }
    get_waiting_lists_output = GetWaitingListsOutput(**data)
    return get_waiting_lists_output
