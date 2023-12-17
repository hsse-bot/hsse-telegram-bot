from typing import NoReturn, List

from sqlalchemy import Engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from data.common.RoleData import RoleData
from data.db.Entities import Role
from data.services.RolesRepository import RolesRepository


class MySqlRolesRepository(RolesRepository):

    def __init__(self, engine: Engine):
        self.engine = engine

    def get_role_by_name(self, role_name: str) -> RoleData:
        with Session(self.engine) as session:
            found_role = session.scalars(select(Role).where(Role.role_name == role_name)).one()
            return RoleData.from_db_role(found_role)

    def create_role(self, role_name: str) -> NoReturn:
        with Session(self.engine) as session:
            role = Role(role_name=role_name)
            session.add(role)
            session.commit()

    def get_role(self, role_id: int) -> RoleData:
        with Session(self.engine) as session:
            found_role = session.scalars(select(Role).where(Role.id == role_id)).one()
            return RoleData.from_db_role(found_role)

    def get_all_roles(self) -> List[RoleData]:
        with Session(self.engine) as session:
            all_roles = []
            for role in session.scalars(select(Role)):
                role_data = RoleData(id=role.id, name=role.role_name)
                all_roles.append(role_data)
            return all_roles

    def delete_role(self, role_id: int) -> NoReturn:
        with Session(self.engine) as session:
            role = select(Role).where(Role.id == role_id)
            if role:
                session.delete(role)
                session.commit()
