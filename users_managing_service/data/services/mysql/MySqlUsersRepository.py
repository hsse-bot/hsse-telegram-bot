from typing import NoReturn, List

from sqlalchemy import Engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from data.common.StudentInfoData import StudentInfoData
from data.common.UserData import UserData
from data.common.UserDelta import UserDelta
from data.db.Entities import User, StudentInfo, BannedUser
from data.services.UserRepository import UserRepository


class UserBannedException(Exception):
    pass


# noinspection PyUnreachableCode
class MySqlUsersRepository(UserRepository):
    def __init__(self, engine: Engine):
        self.engine = engine

    def unban_user(self, tg_id: int):
        with Session(self.engine) as session:
            session.query(BannedUser).filter(BannedUser.tg_id == tg_id).delete()
            session.commit()

    def ban_user(self, tg_id: int) -> NoReturn:
        self.delete_user(tg_id)

        with Session(self.engine) as session:
            session.add(BannedUser(tg_id=tg_id))
            session.commit()

    def create_user(self, user_data: UserData) -> NoReturn:
        with Session(self.engine) as session:
            if session.query(BannedUser).filter(BannedUser.tg_id == user_data.tg_id).count() > 0:
                raise UserBannedException()

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

    def is_user_banned(self, tg_id: int) -> bool:
        with Session(self.engine) as session:
            return session.query(BannedUser).filter(BannedUser.tg_id == tg_id).count() > 0

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

                if delta.student_info_delta.new_group_number is not None:
                    user.student_info.group_number = delta.student_info_delta.new_group_number

            session.commit()
            return UserData.from_db_user(user)

    def delete_user(self, tg_id: int) -> NoReturn:
        with Session(self.engine) as session:
            session.query(User).filter(User.tg_id == tg_id).delete()
            session.commit()

    @staticmethod
    def _assign_student_info_data(user_student_info: StudentInfo, student_info: StudentInfoData) -> NoReturn:
        if student_info is not None:
            if student_info.room_number is not None:
                room_number = student_info.room_number
                user_student_info.room_number = room_number
            if student_info.is_male is not None:
                is_male = student_info.is_male
                user_student_info.is_male = is_male
