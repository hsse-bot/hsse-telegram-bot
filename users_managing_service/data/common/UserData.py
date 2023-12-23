from dataclasses import dataclass
from typing import Optional

from data.common.RoleData import RoleData
from data.common.StudentInfoData import StudentInfoData
from data.db.Entities import User


@dataclass
class UserData:
    name: str
    surname: str
    tg_id: int
    role: RoleData
    student_info: Optional[StudentInfoData]
    score: int
    email: str

    def to_dict(self) -> dict:
        dict_user = {
            "name": self.name,
            "surname": self.surname,
            "tgId": self.tg_id,
            "role": self.role.to_dict(),
            "score": self.score,
            "email": self.email
        }

        if self.student_info is not None:
            dict_user["studentInfo"] = self.student_info.to_dict()

        return dict_user

    @staticmethod
    def from_db_user(user: User):
        return UserData(name=user.name,
                        surname=user.surname,
                        tg_id=user.tg_id,
                        role=RoleData.from_db_role(user.role),
                        score=user.score,
                        email=user.email,
                        student_info=None if user.student_info is None
                        else StudentInfoData.from_db_student_info(user.student_info))
