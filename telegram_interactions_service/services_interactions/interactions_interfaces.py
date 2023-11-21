from abc import ABC, abstractmethod
from typing import NoReturn, List
from ..misc.dataclasses import User, Form, Role, UserDelta, FormTicket, MaterialHelpTicket, NotifyCategory, InputUserData


class UserManagingServiceInteractionInterface(ABC):
    @abstractmethod
    def add_user_to_database(self, user: InputUserData) -> NoReturn:
        pass

    @abstractmethod
    def set_user_role(self, user: User, new_role: Role) -> NoReturn:
        pass

    @abstractmethod
    def add_admin(self, user: User) -> NoReturn:
        pass

    @abstractmethod
    def get_score(self, user: User) -> int | None:
        pass

    @abstractmethod
    def update_user(self, user: User, new_user_data: UserDelta) -> NoReturn:
        pass

    @abstractmethod
    def get_top_scores(self) -> List[User] | None:
        pass

    @abstractmethod
    def get_user_role(self, user: User) -> Role | None:
        pass

    @abstractmethod
    def get_user(self, tg_id: int) -> User | None:
        pass


class FormsManagingServiceInteractionInterface(ABC):
    @abstractmethod
    def create_form(self, form: Form) -> NoReturn:
        pass

    @abstractmethod
    def delete_form(self, form: Form) -> NoReturn:
        pass

    @abstractmethod
    def show_forms(self) -> List[Form]:
        pass

    # Think more about format - dataclass / namedtuple
    # @abstractmethod
    # def export_form(self, form: Form, format: str) -> :
    # pass

    @abstractmethod
    def show_user_tickets(self, user: User) -> list[FormTicket]:
        pass

    @abstractmethod
    def show_form_tickets(self, form: Form) -> List[FormTicket]:
        pass


class MaterialHelpServiceInteractionInterface(ABC):
    @abstractmethod
    def get_ticket(self, user: User) -> MaterialHelpTicket:
        pass

    @abstractmethod
    def get_tickets(self, filters: List) -> List[MaterialHelpTicket]:
        pass


class TelegramNotifierServiceInteractionInterface(ABC):
    @abstractmethod
    def notify(self, category: NotifyCategory, text: str) -> NoReturn:
        pass

    # fill remaining
