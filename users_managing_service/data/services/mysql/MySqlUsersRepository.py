from typing import NoReturn, List
from sqlalchemy import Engine
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import Session
from data.db.Base import Base
from data.common.UserData import UserData
from data.common.UserDelta import UserDelta
from data.common.StudentInfoDelta import StudentInfoDelta
from data.db.entities.User import User
from data.db.entities.StudentInfo import StudentInfo
from data.common.StudentInfoData import StudentInfoData


class MySqlUsersRepository:

    def __init__(self, engine: Engine):
        self.engine = engine

    def create_user(self, user_data: UserData) -> NoReturn:
        with Session(self.engine) as session:
            user = User(
                name=user_data.name,
                surname=user_data.surname,
                role_id=user_data.role.id,
                tg_id=user_data.tg_id,
                role=user_data.role,
                score=user_data.score
            )
            self._assign_student_info_data(user.student_info, user_data.student_info)
            session.add(user)
            session.commit()

    def get_user(self, tg_id: int) -> UserData:
        with Session(self.engine) as session:
            found_user = session.scalars(select(User).where(User.tg_id == tg_id)).one()
            return found_user

    def get_all_users(self) -> List[UserData]:
        with Session(self.engine) as session:
            all_users = []
            for user in session.scalars(select(User)):
                user_data = UserData()
                self._assign_user_data(user, user_data)
                all_users.append(user_data)
            return all_users

    def update_user(self, tg_id: int, delta: UserDelta) -> NoReturn:
        with Session(self.engine) as session:
            user = session.query(User).filter(User.tg_id == tg_id)[0]
            update(User).where(User.tg_id == tg_id).values(
                name=delta.new_name if delta.new_name else user.name,
                surname=delta.new_surname if delta.new_surname else user.surname,
                role_id=delta.new_role_id if delta.new_role_id else user.role_id,
                score=delta.new_score if delta.new_score else user.score
            )
            self._assign_student_info_delta(user.student_info, delta.student_info_delta)

    def delete_user(self, tg_id: int) -> NoReturn:
        with Session(self.engine) as session:
            user = select(User).where(User.tg_id == tg_id)
            session.delete(user)
            session.commit()

    def _assign_user_data(self, user, user_data) -> NoReturn:
        user_data.name = user.name
        user_data.surname = user.surname
        user_data.tg_id = user.tg_id
        user_data.role.id = user.role.id
        user_data.role.name = user.role.role_name
        self._assign_student_info(user.student_info, user_data.student_info)
        user_data.score = user.score

    def _assign_student_info_delta(self, user_student_info: StudentInfo,
                                   student_info_delta: StudentInfoDelta) -> NoReturn:
        if (student_info_delta != None):
            if (student_info_delta.new_room_number != None):
                new_room_number = student_info_delta.new_room_number
                user_student_info.room_number = new_room_number
            if (student_info_delta.new_is_male != None):
                new_is_male = student_info_delta.new_is_male
                user_student_info.is_male = new_is_male

    def _assign_student_info_data(self, user_student_info: StudentInfo, student_info: StudentInfoData) -> NoReturn:
        if (student_info != None):
            if (student_info.room_number != None):
                room_number = student_info.room_number
                user_student_info.room_number = room_number
            if (student_info.is_male != None):
                is_male = student_info.is_male
                user_student_info.is_male = is_male

    def _assign_student_info(self, user_student_info: StudentInfo, user_data_student_info: StudentInfoData) -> NoReturn:
        if (user_student_info != None):
            if (user_student_info.room_number != None):
                room_number = user_student_info.room_number
                user_data_student_info.room_number = room_number
            if (user_student_info.is_male != None):
                is_male = user_student_info.is_male
                user_data_student_info.is_male = is_male
