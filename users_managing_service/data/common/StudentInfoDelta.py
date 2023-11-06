from typing import Optional
from dataclasses import dataclass


@dataclass
class StudentInfoDelta:
    new_room_number: Optional[int]
    new_is_male: Optional[bool]
