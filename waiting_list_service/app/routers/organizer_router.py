from fastapi import APIRouter
from fastapi.params import Depends

from app.managers import organizer_manager
from app.managers.postgres_manager import PostgresManager
from app.schemas.organizer_router_schemas import (
    AddStockInput,
    BuyTicketsInput,
    GetWaitingListsInput,
    GetWaitingListsOutput,
    RemoveStockInput,
)
from app.utils.dependencies import (
    get_postgres_manager,
)

router = APIRouter(tags=["Organizer"], prefix="/organizer")


@router.put("/add-total-stock")
async def add_total_stock(
        add_total_stock_input: AddStockInput,
        postgres_manager: PostgresManager = Depends(get_postgres_manager),
) -> str:
    organizer_manager.add_total_stock(
        add_total_stock_input=add_total_stock_input,
        postgres_manager=postgres_manager,
    )
    return "success"


@router.put("/add-stock")
async def add_stock(
        add_stock_input: AddStockInput,
        postgres_manager: PostgresManager = Depends(get_postgres_manager),
) -> str:
    # TODO If more tickets than current waiting list size are added
    organizer_manager.add_stock(
        add_stock_input=add_stock_input,
        postgres_manager=postgres_manager,
    )
    return "success"


@router.put("/remove-stock")
async def remove_stock(
        remove_stock_input: RemoveStockInput,
        postgres_manager: PostgresManager = Depends(get_postgres_manager),
) -> str:
    # TODO open waiting list if available is 0
    organizer_manager.remove_stock(
        remove_stock_input=remove_stock_input,
        postgres_manager=postgres_manager,
    )
    return "success"


@router.post("/buy-tickets")  # From the waiting list
async def buy_tickets(
        buy_tickets_input: BuyTicketsInput,
        postgres_manager: PostgresManager = Depends(get_postgres_manager),
) -> str:
    organizer_manager.buy_tickets(
        buy_tickets_input=buy_tickets_input,
        postgres_manager=postgres_manager,
    )
    return "success"


# Had to switch to post instead of get because of params handling issue
@router.post("/get-waiting-lists")
async def get_waiting_lists(
        get_waiting_lists_input: GetWaitingListsInput,
        postgres_manager: PostgresManager = Depends(get_postgres_manager),
) -> GetWaitingListsOutput:
    # TODO add before and after filters
    get_waiting_lists_output = organizer_manager.get_waiting_lists(
        get_waiting_lists_input=get_waiting_lists_input,
        postgres_manager=postgres_manager,
    )
    return get_waiting_lists_output

# TODO multiple getters for inventory, offers, events, representations
