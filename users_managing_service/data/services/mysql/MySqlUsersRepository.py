from typing import NoReturn, List

from sqlalchemy import Engine
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import Session

from data.common.StudentInfoData import StudentInfoData
from data.common.StudentInfoDelta import StudentInfoDelta
from data.common.UserData import UserData
from data.common.UserDelta import UserDelta
from data.db.Entities import User, Role, StudentInfo
from data.services.UserRepository import UserRepository


class MySqlUsersRepository(UserRepository):

    def __init__(self, engine: Engine):
        self.engine = engine

    def create_user(self, user_data: UserData) -> NoReturn:
        with Session(self.engine) as session:
            user = User(
                name=user_data.name,
                surname=user_data.surname,
                role_id=user_data.role.id,
                tg_id=user_data.tg_id,
                score=user_data.score
            )
            self._assign_student_info_data(user.student_info, user_data.student_info)
            session.add(user)
            session.commit()

    def get_user(self, tg_id: int) -> UserData:
        with Session(self.engine) as session:
            found_user = session.scalars(select(User).where(User.tg_id == tg_id)).one()
            return UserData.from_db_user(found_user)

    def get_all_users(self) -> List[UserData]:
        with Session(self.engine) as session:
            all_users = []
            for user in session.scalars(select(User)):
                all_users.append(UserData.from_db_user(user))
            return all_users

    def update_user(self, tg_id: int, delta: UserDelta) -> UserData:
        with Session(self.engine) as session:
            user = session.query(User).filter(User.tg_id == tg_id)[0]
            session.query(User).filter(User.tg_id == tg_id).update({
                "name": delta.new_name if delta.new_name else User.name,
                "surname": delta.new_surname if delta.new_surname else User.surname,
                "role_id": delta.new_role_id if delta.new_role_id else User.role_id,
                "score": delta.delta_score + User.score if delta.delta_score
                else delta.new_score
                if delta.new_score else User.score
            })

            if delta.student_info_delta is not None:
                if user.student_info is None:
                    user.student_info = StudentInfo()

                if delta.student_info_delta.new_is_male is not None:
                    user.student_info.is_male = delta.student_info_delta.new_is_male

                if delta.student_info_delta.new_room_number is not None:
                    user.student_info.room_number = delta.student_info_delta.new_room_number

            session.commit()
            return UserData.from_db_user(user)

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

    @staticmethod
    def _assign_student_info_data(user_student_info: StudentInfo, student_info: StudentInfoData) -> NoReturn:
        if student_info is not None:
            if student_info.room_number is not None:
                room_number = student_info.room_number
                user_student_info.room_number = room_number
            if student_info.is_male is not None:
                is_male = student_info.is_male
                user_student_info.is_male = is_male

    @staticmethod
    def _assign_student_info(user_student_info: StudentInfo, user_data_student_info: StudentInfoData) -> NoReturn:
        if user_student_info is not None:
            if user_student_info.room_number is not None:
                room_number = user_student_info.room_number
                user_data_student_info.room_number = room_number
            if user_student_info.is_male is not None:
                is_male = user_student_info.is_male
                user_data_student_info.is_male = is_male
