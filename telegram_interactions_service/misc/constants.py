from typing import Final

from .student_info_fields import StudentInfoField

MAX_CATEGORIES_PER_PAGE: Final[int] = 5
MAX_CATEGORIES_CNT: Final[int] = 13
MAX_ADMINS_PER_PAGE: Final[int] = 5
MAX_PROFILE_FIELD_PER_PAGE: Final[int] = 3
SIZE_OF_USERS_TOP: Final[int] = 10

USER_ROLE_NAME: Final[str] = "user"
ADMIN_ROLE_NAME: Final[str] = "admin"
SUPER_ADMIN_ROLE_NAME: Final[str] = "super_admin"

all_student_info_fields = [
    StudentInfoField("roomNumber", "номер комнаты"),
    StudentInfoField("isMale", "пол"),
    StudentInfoField("groupNumber", "номер группы"),
]

# add_user_errors
USER_SERVICE_400_STATUS_MSG_EXISTING_TG_ID_OR_EMAIL: Final[str] = "User already created with these parameters"
USER_SERVICE_400_STATUS_MSG_ADDING_BANNED_USER: Final[str] = "User banned"
