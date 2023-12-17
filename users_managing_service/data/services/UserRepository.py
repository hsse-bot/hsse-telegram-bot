from abc import ABC, abstractmethod

from data.common.UserData import UserData
from data.common.UserDelta import UserDelta


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserData):
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
    def delete_user(self, tg_id: int):
        pass
