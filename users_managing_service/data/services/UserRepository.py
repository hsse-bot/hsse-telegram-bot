from abc import ABC, abstractmethod
from typing import NoReturn

from data.common.UserData import UserData
from data.common.UserDelta import UserDelta


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserData) -> NoReturn:
        pass

    @abstractmethod
    def ban_user(self, tg_id: int) -> NoReturn:
        pass

    @abstractmethod
    def unban_user(self, tg_id: int) -> NoReturn:
        pass

    @abstractmethod
    def is_user_banned(self, tg_id: int) -> bool:
        pass

    @abstractmethod
    def get_user(self, tg_id: int) -> UserData:
        pass

    @abstractmethod
    def get_all_users(self) -> list[UserData]:
        pass

    @abstractmethod
    def update_user(self, tg_id: int, delta: UserDelta) -> UserData:
        pass

    @abstractmethod
    def delete_user(self, tg_id: int) -> NoReturn:
        pass
