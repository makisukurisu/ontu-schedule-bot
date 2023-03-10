"""This module contains some handy enumerators for bot"""
from enum import Enum


class Statuses(Enum):
    """Conains all statuses that backend may give"""
    OK = "ok"


class Endpoints(Enum):
    """Contains all used endpoints"""
    CHAT_INFO = "/api/chat_info"
    CHAT_CREATE = "/api/chat_create"
    CHAT_UPDATE = "/api/chat_update"

    CHATS_ALL = "/api/chats_all"

    FACULTIES_GET = "/api/faculties_get"

    GROUPS_GET = "/api/groups_get"

    SCHEDULE_GET = "/api/schedule_get"


FACULTY_NAME_INDEX = 1
PAGE_INDEX = 2
