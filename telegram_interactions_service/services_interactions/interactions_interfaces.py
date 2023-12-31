from abc import ABC, abstractmethod
from typing import NoReturn, List
from ..misc.dataclasses import (
    User, Form, Role, UserDelta, FormTicket, MaterialHelpTicket, NotifyCategory,
    RegistrationUserData, Admin
)


class UserManagingServiceInteractionInterface(ABC):
    @abstractmethod
    async def get_role_id(self, role_name: str) -> int:
        pass

    @abstractmethod
    async def get_user(self, tg_id: int) -> User | None:
        pass

    @abstractmethod
    async def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    async def add_user_to_database(self, user: RegistrationUserData) -> NoReturn:
        pass

    @abstractmethod
    async def update_user(self, tg_id: int, new_user_data: UserDelta) -> NoReturn:
        pass

    @abstractmethod
    async def delete_user(self, tg_id: int) -> NoReturn:
        pass

    @abstractmethod
    async def set_role(self, tg_id: int, new_role_id: int) -> NoReturn:
        pass

    @abstractmethod
    async def set_user_user_role(self, tg_id: int) -> NoReturn:
        pass

    @abstractmethod
    async def set_user_admin_role(self, tg_id: int) -> NoReturn:
        pass

    @abstractmethod
    async def is_admin(self, tg_id: int) -> bool:
        pass

    @abstractmethod
    async def get_admins(self) -> List[Admin]:
        pass

    @abstractmethod
    async def get_top_scores(self) -> List[User] | None:
        pass

    @abstractmethod
    async def add_activity_points(self, tg_id: int, points: int) -> NoReturn:
        pass

    @abstractmethod
    async def ban_user(self, tg_id: int) -> NoReturn:
        pass

    @abstractmethod
    async def is_banned(self, tg_id: int) -> bool:
        pass

    @abstractmethod
    async def unban_user(self, tg_id: int) -> NoReturn:
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
    async def notify(self, category_id: int, text: str) -> NoReturn:
        pass

    @abstractmethod
    async def create_category(self, category_name: str) -> NoReturn:
        pass

    @abstractmethod
    async def delete_category(self, category_id: int) -> NoReturn:
        pass

    @abstractmethod
    async def get_category(self, category_id: int) -> NotifyCategory:
        pass

    @abstractmethod
    async def get_all_categories(self) -> List[NotifyCategory]:
        pass

    @abstractmethod
    async def get_user_categories(self, user_tg_id: int) -> List[NotifyCategory]:
        pass

    @abstractmethod
    async def sub_user_to_category(self, user_tg_id: int, category_id: int) -> NoReturn:
        pass

    @abstractmethod
    async def unsub_user_to_category(self, user_tg_id: int, category_id: int) -> NoReturn:
        pass
