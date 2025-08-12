from enum import Enum


class Status(str, Enum):
    waiting = "waiting" #  User in the waiting list
    ready = "ready"     #  User can buy tickets
    left = "left"       #  User left the waiting list (after buying tickets or simply leaving)

def format_list_to_query(l: list) -> str:
    return "('" + "', '".join(l) + "')"