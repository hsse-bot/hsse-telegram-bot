from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Role:
    id: int
    name: str
    is_admin: bool


@dataclass
class StudentInfo:
    room_number: int
    is_male: bool


@dataclass
class User:
    name: str
    surname: str
    tg_id: int
    role: Role
    score: int
    student_info: StudentInfo


@dataclass
class Form:
    id: int
    name: str


@dataclass
class StudentInfoDelta:
    room_number: int
    is_male: bool


@dataclass
class UserDelta:
    new_name: str
    new_surname: str
    new_role_id: int
    student_info_delta: StudentInfoDelta
    new_score: int


@dataclass
class FormTicket:
    form: Form
    author: User
    creation_date: datetime


@dataclass
class Bill:
    photo: str


@dataclass
class MaterialHelpTicket:
    author: User
    bills: List[Bill]
    creation_data: datetime


@dataclass
class NotifyCategory:
    id: int
    name: str
