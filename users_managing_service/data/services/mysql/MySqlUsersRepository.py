from typing import NoReturn, List
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import Session
from data.db.Base import Base
from data.common.UserData import UserData
from data.common.UserDelta import UserDelta
from data.db.entities.User import User

DATABASE_NAME = 'application.mysql'

engine = create_engine(f'mysql+pymysql://{DATABASE_NAME}')


class MySqlUsersRepository(Base):

    def create_user(self, user_data: UserData) -> NoReturn:
        with Session(engine) as session:
            user = User(
                name=user_data.name,
                surname=user_data.surname,
                role_id=user_data.role.id,
                student_info_id=user_data.student_info.id,
                tg_id=user_data.tg_id,
                role=user_data.role,
                student_info=user_data.student_info,
                score=user_data.score
            )
            session.add(user)
            session.commit()

    def get_user(self, tg_id: int) -> UserData:
        with Session(engine) as session:
            found_user = session.query(User).filter(User.tg_id == tg_id)[0]
            session.commit()
        return found_user

    def get_all_users(self) -> List[UserData]:
        all_users = []
        with Session(engine) as session:
            for row in session.execute(select(UserData)).first():
                all_users.append(row)
            session.commit()
        return all_users

    def update_user(self, tg_id: int, delta: UserDelta) -> NoReturn:
        with Session(engine) as session:
            update(UserData).where(User.tg_id == tg_id).values(
                name=delta.new_name,
                surname=delta.new_surname,
                role_id=delta.new_role_id,
                student_info=delta.student_info_delta,
                score=delta.new_score
            )
            session.commit()

    def delete_user(self, tg_id: int) -> NoReturn:
        with Session(engine) as session:
            user = select(UserData).where(User.tg_id == tg_id)
            session.delete(user)
            session.commit()
