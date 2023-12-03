import aiohttp
from telegram_interactions_service.services_interactions import interactions_interfaces
from typing import NoReturn, List
from ..misc.dataclasses import User, Form, Role, UserDelta, FormTicket, RegistrationUserData


class UserManagingServiceInteraction(interactions_interfaces.UserManagingServiceInteractionInterface):
    def add_user_to_database(self, user: RegistrationUserData) -> NoReturn:
        pass

    def set_user_role(self, user: User, new_role: Role) -> NoReturn:
        pass

    def add_admin(self, user: User) -> NoReturn:
        pass

    def get_score(self, user: User) -> int | None:
        pass

    def update_user(self, user: User, new_user_data: UserDelta) -> NoReturn:
        pass

    def get_top_scores(self) -> List[User] | None:
        pass

    def get_user_role(self, user: User) -> Role | None:
        pass

    def get_user(self, tg_id: int) -> User | None:
        pass

    def is_admin(self, tg_id) -> bool:
        return True
