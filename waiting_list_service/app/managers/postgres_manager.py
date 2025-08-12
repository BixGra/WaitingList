import psycopg2
from psycopg2.errors import (
    UniqueViolation,
)
from psycopg2.extras import RealDictCursor

from app.schemas.organizer_router_schemas import Status
from app.utils.errors import (
    InventoryNotFoundError,
    MaximumWantedTicketsError,
    NotInWaitingListError,
    UniqueViolationError,
    WaitingListNotOpenError,
)
from app.utils.tools import format_list_to_query


class PostgresManager:
    def __init__(
            self,
            host: str,
            port: int,
            dbname: str,
            user: str,
            password: str,
    ):
        try:
            self.conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
        except psycopg2.Error:
            raise

    """USERS FUNCTIONS"""
    def join_list(
            self,
            user_id: str,
            offer_id: str,
            representation_id: str,
            tickets_wanted: int,
            status: Status = 'waiting',
    ) -> None:
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"""SELECT inventory.waiting_list_open, offers.max_quantity_per_order FROM inventory
                    JOIN offers ON inventory.offer_id = offers.offer_id
                    WHERE inventory.offer_id = '{offer_id}'
                    AND inventory.representation_id = '{representation_id}'"""
                )
                if result := cursor.fetchone():
                    waiting_list_open, max_quantity_per_order = result
                    if waiting_list_open:
                        if tickets_wanted <= max_quantity_per_order:
                            try:
                                cursor.execute(
                                    f"""INSERT INTO waiting_list (user_id, offer_id, representation_id, tickets_wanted, status)
                                    VALUES ('{user_id}', '{offer_id}', '{representation_id}', '{tickets_wanted}', '{status}')"""
                                )
                                self.conn.commit()
                            except UniqueViolation:
                                # TODO User wants to rejoin the waiting list after leaving it
                                #   If status is "left"
                                #     Update row : set status to "waiting" and reset created_at
                                #   Else
                                #     Raise
                                raise UniqueViolationError
                        else:
                            raise MaximumWantedTicketsError
                    else:
                        raise WaitingListNotOpenError
                else:
                    raise InventoryNotFoundError


    def leave_list(
            self,
            user_id: str,
            offer_id: str,
            representation_id: str,
    ) -> None:
        # TODO First check if user is in this waiting list else raise NotInWaitingListError
        #   Also check if status
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"""UPDATE waiting_list
                    SET status = 'left'
                    WHERE user_id = '{user_id}'
                    AND offer_id = '{offer_id}'
                    AND representation_id = '{representation_id}'"""
                )
                self.conn.commit()

    def get_all_status(
            self,
            user_id: str,
    ) -> list[dict]:
        with self.conn:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    f"""SELECT offer_id, representation_id FROM waiting_list
                    WHERE user_id = '{user_id}'"""
                )
                return cursor.fetchall()

    def get_status(
            self,
            user_id: str,
            offer_id: str,
            representation_id: str,
    ) -> tuple[int, str, int]:
        """
        Return waiting_list_position, status, tickets_wanted
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"""SELECT created_at, status, tickets_wanted FROM waiting_list
                    WHERE user_id = '{user_id}' 
                    AND offer_id = '{offer_id}'
                    AND representation_id = '{representation_id}'"""
                )
                if response := cursor.fetchone():
                    created_at, status, tickets_wanted = response
                    cursor.execute(
                        f"""SELECT COUNT(*) FROM waiting_list
                        WHERE offer_id = '{offer_id}'
                        AND representation_id = '{representation_id}'
                        AND status = 'waiting'
                        AND created_at < '{created_at}'"""
                    )
                    return 1+cursor.fetchone()[0], status, tickets_wanted
                else:
                    raise NotInWaitingListError

    def get_available_stock(
            self,
            offer_id: str,
            representation_id: str,
    ) -> int:
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"""SELECT available_stock FROM inventory
                    WHERE offer_id = '{offer_id}'
                    AND representation_id = '{representation_id}'"""
                )
                if response := cursor.fetchone():
                    return response[0]
                else:
                    raise InventoryNotFoundError

    def get_eligible_users(
            self,
            offer_id: str,
            representation_id: str,
            available_stock: int,
    ) -> list[str]:
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"""SELECT user_id FROM (
                            SELECT user_id, status, SUM(tickets_wanted) OVER (ORDER BY created_at) as cum_sum FROM waiting_list
                            WHERE offer_id = '{offer_id}'
                            AND representation_id = '{representation_id}'
                            AND status IN ('waiting', 'ready')
                        )
                        WHERE cum_sum < {available_stock}
                        AND status = 'waiting'"""
                )
                user_ids = []
                if result := cursor.fetchall():
                    user_ids = list(map(lambda x: x[0], result))
                    cursor.execute(
                        f"""UPDATE waiting_list
                        SET status = 'ready'
                        WHERE user_id IN {format_list_to_query(user_ids)}"""
                    )
                return user_ids

    """ORGANIZERS FUNCTIONS"""
    def add_total_stock(
            self,
            offer_id: str,
            representation_id: str,
            stock_amount: int,
    ) -> None:
        with self.conn:
            with self.conn.cursor() as cursor:
                # TODO Check if exists
                cursor.execute(
                    f"""UPDATE inventory
                    SET (total_stock, available_stock) = (total_stock + {stock_amount}, available_stock + {stock_amount})
                    WHERE offer_id = '{offer_id}'
                    AND representation_id = '{representation_id}'"""
                )

    def add_stock(
            self,
            offer_id: str,
            representation_id: str,
            stock_amount: int,
    ) -> None:
        with self.conn:
            with self.conn.cursor() as cursor:
                # TODO Check if exists
                cursor.execute(
                    f"""UPDATE inventory
                    SET available_stock = available_stock + {stock_amount}
                    WHERE offer_id = '{offer_id}'
                    AND representation_id = '{representation_id}'"""
                )

    def remove_stock(
            self,
            offer_id: str,
            representation_id: str,
            stock_amount: int,
    ) -> None:
        with self.conn:
            with self.conn.cursor() as cursor:
                # TODO Check if exists
                cursor.execute(
                    f"""UPDATE inventory
                    SET available_stock = available_stock + {stock_amount}
                    WHERE offer_id = '{offer_id}'
                    AND representation_id = '{representation_id}'"""
                )

    def get_waiting_lists(
            self,
            user_ids: list[str],
            offer_ids: list[str],
            representation_ids: list[str],
            event_ids: list[str],
            status: list[Status],
    ) -> list[dict]:
        with self.conn:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # TODO Check if exists
                filters = ""
                if any([user_ids, offer_ids, representation_ids, event_ids, status]):
                    filters = []
                    if user_ids:
                        filters.append(f"waiting_list.user_id IN {format_list_to_query(user_ids)}")
                    if offer_ids:
                        filters.append(f"waiting_list.offer_id IN {format_list_to_query(offer_ids)}")
                    if representation_ids:
                        filters.append(f"waiting_list.representation_id IN {format_list_to_query(representation_ids)}")
                    if status:
                        filters.append(f"waiting_list.status IN {format_list_to_query(status)}")
                    if event_ids:
                        filters.append(f"representations.event_id IN {format_list_to_query(event_ids)}")
                    filters = "WHERE " + " AND ".join(filters)
                cursor.execute(
                    f"""SELECT
                        waiting_list.user_id,
                        waiting_list.offer_id,
                        waiting_list.representation_id,
                        waiting_list.created_at,
                        waiting_list.tickets_wanted,
                        waiting_list.status,
                        representations.event_id
                    FROM waiting_list
                    JOIN representations ON representations.id = waiting_list.representation_id
                    {filters}
                    ORDER BY
                        representations.event_id,
                        waiting_list.offer_id,
                        waiting_list.representation_id,
                        waiting_list.status,
                        waiting_list.created_at
                    """
                )
                waiting_lists = cursor.fetchall()
                return waiting_lists