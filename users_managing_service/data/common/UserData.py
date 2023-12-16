from dataclasses import dataclass
from typing import Optional

from data.common.RoleData import RoleData
from data.common.StudentInfoData import StudentInfoData


@dataclass
class UserData:
    name: str
    surname: str
    tg_id: int
    role: RoleData
    student_info: Optional[StudentInfoData]
    score: int
    
