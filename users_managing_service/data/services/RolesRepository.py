from abc import ABC


class RolesRepository(ABC):
    def create_role(self, role_name: str) -> RoleData:
        raise NotImplementedError()
    
    def delete_role(self, role_id: int):
        raise NotImplementedError()
    
    def get_role(self, role_id: int):
        raise NotImplementedError()
    
    def get_all_roles(self) -> list[RoleData]:
        raise NotImplementedError()
    