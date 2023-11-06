from dataclasses import dataclass
from typing import Optional

from data.common.StudentInfoDelta import StudentInfoDelta


@dataclass
class UserDelta:
    new_name: Optional[str]
    new_surname: Optional[str]
    new_role_id: Optional[int]
    student_info_delta: Optional[StudentInfoDelta]
    new_score: Optional[int]
    