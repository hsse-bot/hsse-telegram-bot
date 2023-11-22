import aiohttp
from telegram_interactions_service.services_interactions import interactions_interfaces
from typing import NoReturn, List
from ..misc.dataclasses import User, Form, Role, UserDelta, FormTicket, InputUserData


class UserManagingServiceInteraction(interactions_interfaces.UserManagingServiceInteractionInterface):
    async def add_user_to_database(self, user: InputUserData) -> NoReturn:
        pass

    async def set_user_role(self, user: User, new_role: Role) -> NoReturn:
        pass

    async def add_admin(self, user: User) -> NoReturn:
        pass

    async def get_score(self, user: User) -> int | None:
        pass

    async def update_user(self, user: User, new_user_data: UserDelta) -> NoReturn:
        pass

    async def get_top_scores(self) -> List[User] | None:
        pass

    async def get_user_role(self, user: User) -> Role | None:
        pass

    async def get_user(self, tg_id: int) -> User | None:
        pass
