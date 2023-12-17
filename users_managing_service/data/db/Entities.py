from typing import Optional, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from data.db.Base import Base


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(32))
    surname: Mapped[str] = mapped_column(String(32))
    role_id: Mapped[int] = mapped_column()
    student_info_id: Mapped[Optional[int]] = mapped_column()
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    student_info_id: Mapped[Optional[int]] = mapped_column(ForeignKey("student_additional_info.id"))
    role: Mapped["Role"] = relationship(
        back_populates="users"
    )
    student_info: Mapped[Optional["StudentInfo"]] = relationship(
        back_populates="user", cascade="all"
    )
    score: Mapped[int] = mapped_column()


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(32))
    users: Mapped[List[User]] = relationship(
        back_populates="role", cascade="all"
    )


class StudentInfo(Base):
    __tablename__ = "student_additional_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_number: Mapped[int] = mapped_column()
    is_male: Mapped[bool] = mapped_column()
    user: Mapped[User] = relationship(
        back_populates="student_info", cascade="all"
    )
