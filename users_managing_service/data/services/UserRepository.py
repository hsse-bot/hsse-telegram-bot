import ctypes
from abc import ABC


class UserRepository(ABC):
    def create_user(self, user: UserData):
        raise NotImplementedError()
    
    def get_user(self, tg_id: int):
        raise NotImplementedError()
    
    def get_all_users(self) -> list[UserData]:
        raise NotImplementedError()
    
    def update_user(self, tg_id: int, delta: UserDelta) -> UserData:
        raise NotImplementedError()
    
    def delete_user(self, tg_id: int):
        raise NotImplementedError()