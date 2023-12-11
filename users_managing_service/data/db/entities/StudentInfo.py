from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class StudentInfo:
    __tablename__ = "students_additional_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_number: Mapped[int] = mapped_column()
    is_male: Mapped[bool] = mapped_column()
