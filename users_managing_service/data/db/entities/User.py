from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from typing import Optional
from users_managing_service.data.db import Base
from users_managing_service.data.db.entities import StudentInfo
from users_managing_service.data.db.entities import Role


class User(Base):
    __tablename__ = "user_account"

    name: Mapped[str] = mapped_column(String(32))
    surname: Mapped[str] = mapped_column(String(32))
    role_id: Mapped[int] = mapped_column(primary_key=True)
    student_info_id: Mapped[Optional[int]] = mapped_column()
    tg_id: Mapped[int] = mapped_column()
    role: Mapped[Role] = mapped_column()
    student_info: Mapped[StudentInfo] = mapped_column()
    score: Mapped[int] = mapped_column()