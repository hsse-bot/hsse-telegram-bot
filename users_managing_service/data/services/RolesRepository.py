from abc import ABC

from data.common.RoleData import RoleData


class RolesRepository(ABC):
    def create_role(self, role_name: str) -> RoleData:
        pass
    
    def delete_role(self, role_id: int):
        pass
    
    def get_role(self, role_id: int):
        pass
    
    def get_all_roles(self) -> list[RoleData]:
        pass
    