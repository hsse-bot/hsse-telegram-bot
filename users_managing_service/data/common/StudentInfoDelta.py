from dataclasses import dataclass
from typing import Optional


@dataclass
class StudentInfoDelta:
    new_room_number: Optional[int]
    new_is_male: Optional[bool]
    new_group_number: Optional[str]
