from typing import List
from material_help_service.data.common.AttachmentData import AttachmentData
from dataclasses import dataclass


@dataclass
class TicketData:
    id: int
    author_th_id: int
    created_at: int
    review_message: str
    ticket_text: str
    attachments: List[AttachmentData]
    is_paper_included: bool
