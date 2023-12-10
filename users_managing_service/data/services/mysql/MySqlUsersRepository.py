from typing import NoReturn, List
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import Session
from data.db.Base import Base
from data.common.UserData import UserData
from data.common.StudentInfoData import StudentInfoData
from data.common.UserDelta import UserDelta
from data.db.entities.User import User
from data.db.entities.StudentInfo import StudentInfo
from data.common.StudentInfoData import StudentInfoData

DATABASE_NAME = 'application.mysql'

engine = create_engine(f'mysql+pymysql://{DATABASE_NAME}')


class MySqlUsersRepository(Base):

    def create_user(self, user_data: UserData) -> NoReturn:
        with Session(engine) as session:
            user = User(
                name=user_data.name,
                surname=user_data.surname,
                role_id=user_data.role.id,
                tg_id=user_data.tg_id,
                role=user_data.role,
                score=user_data.score
            )
            self.check_student_info_data(user, user_data)
            session.add(user)
            session.commit()

    def get_user(self, tg_id: int) -> UserData:
        with Session(engine) as session:
            found_user = session.query(User).filter(User.tg_id == tg_id)[0]
        return found_user

    def get_all_users(self) -> List[UserData]:
        all_users = []
        with Session(engine) as session:
            for user in session.scalars(select(User)):
                user_data = UserData()
                user_data.name = user.name
                user_data.surname = user.surname
                user_data.tg_id = user.tg_id
                user_data.role.id = user.role.id
                user_data.role.name = user.role.role_name
                self.check_student_info(user, user_data)
                user_data.score = user.score
                all_users.append(user_data)
        return all_users

    def update_user(self, tg_id: int, delta: UserDelta) -> NoReturn:
        with Session(engine) as session:
            user = session.query(User).filter(User.tg_id == tg_id)[0]
            update(User).where(User.tg_id == tg_id).values(
                name=delta.new_name if delta.new_name else user.name,
                surname=delta.new_surname if delta.new_surname else user.surname,
                role_id=delta.new_role_id if delta.new_role_id else user.role_id,
                score=delta.new_score if delta.new_score else user.score
            )
            self.check_student_info_delta(user, delta)

    def delete_user(self, tg_id: int) -> NoReturn:
        with Session(engine) as session:
            user = select(User).where(User.tg_id == tg_id)
            session.delete(user)
            session.commit()

    def check_student_info_delta(self, user: User, user_delta: UserDelta) -> NoReturn:
        if (user_delta.student_info_delta != None):
            if (user_delta.student_info_delta.new_room_number != None):
                new_room_number = user_delta.student_info_delta.new_room_number
                user.student_info.room_number = new_room_number
            if (user_delta.student_info_delta.new_is_male != None):
                new_is_male = user_delta.student_info_delta.new_is_male
                user.student_info.is_male = new_is_male

    def check_student_info_data(self, user: User, user_data: UserData) -> NoReturn:
        if (user_data.student_info != None):
            if (user_data.student_info.room_number != None):
                room_number = user_data.student_info.room_number
                user.student_info.room_number = room_number
            if (user_data.student_info.is_male != None):
                is_male = user_data.student_info.is_male
                user.student_info.is_male = is_male

    def check_student_info(self, user: User, user_data: UserData) -> NoReturn:
        if (user.student_info != None):
            if (user.student_info.room_number != None):
                room_number = user.student_info.room_number
                user_data.student_info.room_number = room_number
            if (user.student_info.is_male != None):
                is_male = user.student_info.is_male
                user_data.student_info.is_male = is_male
