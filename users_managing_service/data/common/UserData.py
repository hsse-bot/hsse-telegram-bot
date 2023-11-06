from dataclasses import dataclass
from typing import Optional


@dataclass
class UserData:
    name: str
    surname: str
    tg_id: str
    role: RoleData
    student_info: Optional[RoleData]
    score: int
    