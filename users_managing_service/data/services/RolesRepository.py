from abc import ABC, abstractmethod
from typing import NoReturn

from data.common.RoleData import RoleData


class RolesRepository(ABC):
    @abstractmethod
    def create_role(self, role_name: str) -> RoleData:
        pass

    @abstractmethod
    def delete_role(self, role_id: int) -> NoReturn:
        pass

    @abstractmethod
    def get_role(self, role_id: int) -> RoleData:
        pass

    @abstractmethod
    def get_all_roles(self) -> list[RoleData]:
        pass

    @abstractmethod
    def get_role_by_name(self, role_name: str) -> RoleData:
        pass
    