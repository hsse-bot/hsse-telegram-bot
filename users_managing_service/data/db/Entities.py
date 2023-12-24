from typing import Optional, List

from sqlalchemy import String, ForeignKey, Column, BigInteger, Integer, Boolean
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    surname = Column(String(32), nullable=False)
    role_id = Column(BigInteger, nullable=False)
    student_info_id = Column(BigInteger, nullable=False)
    tg_id = Column(BigInteger, unique=True, nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    role_id = Column(BigInteger, ForeignKey("roles.id"), nullable=False)
    student_info_id = Column(BigInteger, ForeignKey("student_additional_info.id"))
    score = Column(Integer, default=0, nullable=False)
    role: Mapped["Role"] = relationship(
        back_populates="users"
    )
    student_info: Mapped[Optional["StudentInfo"]] = relationship(
        back_populates="user", cascade="all"
    )


class BannedUser(Base):
    __tablename__ = "banned_users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)


class Role(Base):
    __tablename__ = "roles"

    id = Column(BigInteger, primary_key=True)
    role_name = Column(String(32), unique=True, nullable=False)
    users: Mapped[List[User]] = relationship(
        back_populates="role", cascade="all"
    )


class StudentInfo(Base):
    __tablename__ = "student_additional_info"

    id = Column(BigInteger, primary_key=True)
    room_number = Column(Integer)
    is_male = Column(Boolean)
    group_number = Column(String(32))
    user: Mapped[User] = relationship(
        back_populates="student_info", cascade="all"
    )
