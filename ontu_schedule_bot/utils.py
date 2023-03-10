"""This is a utils module, it contains Requests and pagination for bot"""
from urllib.parse import urljoin
import math
import requests

from secret_config import API_URL
from enums import Statuses, Endpoints

import classes

import telegram


# region Requests
class BaseRequester:
    """Defines url for requests and method of request"""
    _url: str = API_URL
    _method: str = "POST"

    session = requests.Session()

    def check_response(self, response: requests.Response):
        """
            Method that checks response
            If we get non 200 response - raises ValueError
        """
        if response.status_code != 200:
            raise ValueError(
                f"Received non OK response ({response.status_code})",
                response,
                response.content
            )
        return response

    def make_request(self, endpoint: str, **kwargs):
        """Method for making and getting requests"""
        method: str = self._method or kwargs.pop('method', '')
        if not isinstance(method, (str, bytes, )):
            raise ValueError(
                "Please don't override method with non str/bytes"
            )

        url = urljoin(self._url, endpoint)

        response = self.session.request(
            url=url,
            method=method,
            data=kwargs.pop('data', None),
            json=kwargs.pop('json', None),
            **kwargs
        )

        return self.check_response(response=response)


class Getter(BaseRequester):
    """Class that handles getting and sending messages to admin server"""

    def get_chat(
            self,
            chat_id: int) -> classes.Chat | None:
        """Method to get information about a user"""
        response = self.make_request(
            endpoint=Endpoints.CHAT_INFO.value,
            json={
                'chat_id': chat_id
            }
        )

        answer = response.json()
        if not answer:
            return None
        return classes.Chat.from_json(json_dict=answer)

    def get_faculties(
            self) -> list[classes.Faculty]:
        """Method to get a list of faculties"""
        response = self.make_request(
            endpoint=Endpoints.FACULTIES_GET.value
        )

        answer: list[dict] = response.json()
        faculties: list[classes.Faculty] = []
        for faculty in answer:
            faculties.append(
                classes.Faculty.from_json(
                    faculty
                )
            )
        return faculties

    def get_groups(
            self,
            faculty_name: str) -> list[classes.Group]:
        """This method returns a list of group from faculty name"""
        response = self.make_request(
            endpoint=Endpoints.GROUPS_GET.value,
            json={
                "faculty_name": faculty_name
            }
        )

        answer: list[dict] = response.json()
        groups: list[classes.Group] = []
        for group in answer:
            groups.append(
                classes.Group.from_json(
                    group
                )
            )
        return groups

    def get_all_chats(
            self) -> list[classes.Chat]:
        """This method returns all Telegram Chats with data about them"""
        response = self.make_request(
            endpoint=Endpoints.CHATS_ALL.value
        )

        answer: list[dict] = response.json()
        chat_list: list[classes.Chat] = []
        for group in answer:
            chat_list.append(
                classes.Chat.from_json(
                    group
                )
            )
        return chat_list

    def get_schedule(
            self,
            group: classes.Group) -> classes.Schedule:
        """This method gets schedule for some specific group (schedule)"""
        response = self.make_request(
            endpoint=Endpoints.SCHEDULE_GET.value,
            json={
                'group': group.name,
                'faculty': group.faculty.name
            }
        )

        answer: dict = response.json()
        return classes.Schedule.from_json(answer)


class Setter(BaseRequester):
    """A class for updating/writing data to admin"""

    def new_chat(
            self,
            chat: telegram.Chat
        ) -> classes.Chat|dict|None:
        """Creates a new chat, returns response from server"""
        response = self.make_request(
            endpoint=Endpoints.CHAT_CREATE.value,
            json={
                'chat_id': chat.id,
                'chat_name': chat.effective_name,
                'chat_info': chat.to_json(),
            }
        )
        answer: dict = response.json()
        if answer.pop('status', '') == Statuses.OK.value:
            return Getter().get_chat(chat.id)
        return answer

    def set_chat_group(
            self,
            chat: telegram.Chat,
            group: classes.Group,
            is_active: bool = True) -> classes.Subscription | dict:
        """Updates subscription info for chat"""
        response = self.make_request(
            endpoint=Endpoints.CHAT_UPDATE.value,
            json={
                "chat_id": chat.id,
                "group": {
                    "name": group.name,
                    "faculty": group.faculty.name
                },
                "is_active": is_active,
            }
        )

        answer: dict = response.json()
        if answer.pop('status', '') == Statuses.OK.value:
            return classes.Subscription.from_json(answer)
        return answer

# endregion


# region Pagination
PAGE_SIZE = 10


def get_number_of_pages(list_of_elements: list[object]) -> int:
    """Get's number of pages from some list"""
    return math.ceil(len(list_of_elements) / PAGE_SIZE)

def get_current_page(list_of_elements: list[object], page: int = 0):
    """Returns current part of list divided on pages"""
    if len(list_of_elements) <= PAGE_SIZE:
        return list_of_elements

    return list_of_elements[page*PAGE_SIZE:(page+1)*PAGE_SIZE]

# endregion


# region Common

def get_chat_by_tg_chat(
        chat_id: int):
    """A method to get a chat by chat_id"""
    chat = Getter().get_chat(
        chat_id=chat_id
    )
    if not chat:
        raise ValueError("????????-?????????? - ?????????????? ?? ??????????????: /start")
    return chat

# endregion
