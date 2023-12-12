from abc import ABC

from data.common.UserData import UserData
from data.common.UserDelta import UserDelta


class UserRepository(ABC):
    def create_user(self, user: UserData):
        pass
    
    def get_user(self, tg_id: int):
        pass
    
    def get_all_users(self) -> list[UserData]:
        pass
    
    def update_user(self, tg_id: int, delta: UserDelta) -> UserData:
        pass
    
    def delete_user(self, tg_id: int):
        pass