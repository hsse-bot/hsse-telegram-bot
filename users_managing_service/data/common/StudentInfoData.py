from dataclasses import dataclass

from data.db.Entities import StudentInfo


@dataclass
class StudentInfoData:
    room_number: int
    is_male: bool
    group_number: str

    @staticmethod
    def from_db_student_info(info: StudentInfo):
        return StudentInfoData(
            room_number=info.room_number,
            is_male=info.is_male,
            group_number=info.group_number
        )

    def to_dict(self) -> dict:
        return {
            "roomNumber": self.room_number,
            "isMale": self.is_male,
            "groupNumber": self.group_number
        }
