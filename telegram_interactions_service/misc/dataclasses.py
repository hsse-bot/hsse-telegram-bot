from pydantic import BaseModel, validator
from dataclasses import dataclass
from datetime import datetime
from typing import List
import re
from telegram_interactions_service.exceptions import BadRegistrationInput


class Role(BaseModel):
    id: int
    name: str


class StudentInfo(BaseModel):
    roomNumber: int
    isMale: bool
    groupNumber: str


def generate_student_info(data: dict) -> StudentInfo:
    return StudentInfo(roomNumber=data['roomNumber'],
                       isMale=data['isMale'],
                       groupNumber=data['groupNumber']
                       )


class User(BaseModel):
    name: str
    surname: str
    email: str
    tg_id: int
    role: Role
    score: int
    student_info: StudentInfo | None


class Form(BaseModel):
    id: int
    name: str


class StudentInfoDelta(BaseModel):
    newRoomNumber: int
    newIsMale: bool
    newGroupNumber: str


def generate_delta_student_info(data: dict) -> StudentInfoDelta:
    return StudentInfoDelta(newRoomNumber=data['roomNumber'],
                            newIsMale=data['isMale'],
                            new_groupNumber=data['newGroupNumber']
                            )


class UserDelta(BaseModel):
    newName: str
    newSurname: str
    newRoleId: int
    studentInfoDelta: StudentInfoDelta
    newScore: int
    deltaScore: int


class FormTicket(BaseModel):
    form: Form
    author: User
    creation_date: datetime


class Bill(BaseModel):
    photo: str


class MaterialHelpTicket(BaseModel):
    author: User
    bills: List[Bill]
    creation_data: datetime


class NotifyCategory(BaseModel):
    id: int
    name: str


class Admin(BaseModel):
    tg_id: int
    note: str


class RegistrationUserData(BaseModel):
    name: str
    surname: str
    # group: str
    email_address: str
    tg_id: int

    @validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.isalpha():
            raise BadRegistrationInput("Name must contain only letters")
        return value

    @validator("surname")
    @classmethod
    def validate_surname(cls, value: str) -> str:
        if not value.isalpha():
            raise BadRegistrationInput("Surname must contain only letters")
        return value

    # @validator("group")
    # @classmethod
    # def validate_group(cls, value: str) -> str:
    #     if not bool(re.fullmatch(r'\w\d\d-\d\d\d', value)):
    #         raise BadRegistrationInput("Group must be special format")
    #     return value

    @validator("email_address")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not bool(re.fullmatch(r"^[-\w\.]+@phystech.edu", value)):
            raise BadRegistrationInput("Email is invalid")
        return value
