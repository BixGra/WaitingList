ERRORS = {
    "U01": {
        "title": "User is already in the waiting list for this offer and representation",
        "status_code": 403,
    },
    "U02": {
        "title": "Waiting list is not open because tickets are still available for this offer and representation",
        "status_code": 404,
    },
    "U03": {
        "title": "User wants too many tickets. This offer does not allow that amount of tickets.",
        "status_code": 403,
    },
    "U04": {
        "title": "User must want at least one ticket.",
        "status_code": 403,
    },
    "U05": {
        "title": "User is not in this waiting list.",
        "status_code": 404,
    },
    "U06": {
        "title": "User is in this waiting list but not ready yet.",
        "status_code": 403,
    },
    "O01": {
        "title": "Inventory not found for given offer_id and representation_id.",
        "status_code": 404,
    },
    "O02": {
        "title": "Can't add negative or null amount of stock.",
        "status_code": 403,
    },
    "O03": {
        "title": "Can't remove negative or null amount of stock.",
        "status_code": 403,
    },
    "O04": {
        "title": "Can't remove more stock than available.",
        "status_code": 403,
    },
    "O05": {
        "title": "Unknown status.",
        "status_code": 404,
    },
}

class WaitingListError(Exception):
    def __init__(self, error_code: str):
        self.error_code = error_code
        error = ERRORS.get(self.error_code, {})
        self.status_code = error.get("status_code", "500")
        self.title = error.get("title", "Unknown Error")

    def __str__(self):
        return f"{self.error_code} : {self.title}"

    def __repr__(self):
        return str(self)


class UniqueViolationError(WaitingListError):
    def __init__(self):
        super().__init__("U01")


class WaitingListNotOpenError(WaitingListError):
    def __init__(self):
        super().__init__("U02")


class MaximumWantedTicketsError(WaitingListError):
    def __init__(self):
        super().__init__("U03")


class MinimumWantedTicketsError(WaitingListError):
    def __init__(self):
        super().__init__("U04")


class NotInWaitingListError(WaitingListError):
    def __init__(self):
        super().__init__("U05")


class NotReadyError(WaitingListError):
    def __init__(self):
        super().__init__("U06")


class InventoryNotFoundError(WaitingListError):
    def __init__(self):
        super().__init__("O01")


class NegativeAddStockError(WaitingListError):
    def __init__(self):
        super().__init__("O02")


class NegativeRemoveStockError(WaitingListError):
    def __init__(self):
        super().__init__("O03")


class RemoveStockValueError(WaitingListError):
    def __init__(self):
        super().__init__("O04")


class UnknownStatusError(WaitingListError):
    def __init__(self):
        super().__init__("O05")
