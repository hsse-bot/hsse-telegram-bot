from abc import ABC, abstractmethod
from typing import NoReturn, List
from ..misc.dataclasses import User, Form, Role, UserDelta, FormTicket, MaterialHelpTicket, NotifyCategory, \
    InputUserData


class UserManagingServiceInteractionInterface(ABC):
    @abstractmethod
    async def add_user_to_database(self, user: InputUserData) -> NoReturn:
        pass

    @abstractmethod
    async def set_user_role(self, user: User, new_role: Role) -> NoReturn:
        pass

    @abstractmethod
    async def add_admin(self, user: User) -> NoReturn:
        pass

    @abstractmethod
    async def get_score(self, user: User) -> int | None:
        pass

    @abstractmethod
    async def update_user(self, user: User, new_user_data: UserDelta) -> NoReturn:
        pass

    @abstractmethod
    async def get_top_scores(self) -> List[User] | None:
        pass

    @abstractmethod
    async def get_user_role(self, user: User) -> Role | None:
        pass

    @abstractmethod
    async def get_user(self, tg_id: int) -> User | None:
        pass


class FormsManagingServiceInteractionInterface(ABC):
    @abstractmethod
    async def create_form(self, form: Form) -> NoReturn:
        pass

    @abstractmethod
    async def delete_form(self, form: Form) -> NoReturn:
        pass

    @abstractmethod
    async def show_forms(self) -> List[Form]:
        pass

    # Think more about format - dataclass / namedtuple
    # @abstractmethod
    # async def export_form(self, form: Form, format: str) -> :
    # pass

    @abstractmethod
    async def show_user_tickets(self, user: User) -> List[FormTicket]:
        pass

    @abstractmethod
    async def show_form_tickets(self, form: Form) -> List[FormTicket]:
        pass


class MaterialHelpServiceInteractionInterface(ABC):
    @abstractmethod
    async def get_ticket(self, user: User) -> MaterialHelpTicket:
        pass

    @abstractmethod
    async def get_tickets(self, filters: List) -> List[MaterialHelpTicket]:
        pass


class TelegramNotifierServiceInteractionInterface(ABC):
    @abstractmethod
    async def notify(self, category: NotifyCategory, text: str) -> NoReturn:
        pass

    @abstractmethod
    async def create_category(self, category: NotifyCategory) -> NoReturn:
        pass

    @abstractmethod
    async def delete_category(self, category: NotifyCategory) -> NoReturn:
        pass

    @abstractmethod
    async def get_all_categories(self) -> List[NotifyCategory]:
        pass

    @abstractmethod
    async def get_user_categories(self, user: User) -> List[NotifyCategory]:
        pass

    @abstractmethod
    async def sub_user_to_category(self, user: User, category: NotifyCategory) -> NoReturn:
        pass

    @abstractmethod
    async def unsub_user_to_category(self, user: User, category: NotifyCategory) -> NoReturn:
        pass
