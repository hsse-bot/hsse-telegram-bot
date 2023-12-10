from dataclasses import dataclass
from typing import Optional

from data.common.RoleData import RoleData


@dataclass
class UserData:
    name: str
    surname: str
    tg_id: int
    role: RoleData
    student_info: Optional[StudentInfo]
    score: int
    
