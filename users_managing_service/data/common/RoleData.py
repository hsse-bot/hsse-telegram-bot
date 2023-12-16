from dataclasses import dataclass

from data.db.Entities import Role


@dataclass
class RoleData:
    id: int
    name: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }

    @staticmethod
    def from_db_role(role: Role):
        return RoleData(id=role.id, name=role.role_name)