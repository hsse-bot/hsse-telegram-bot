from typing import List
from material_help_service.data.common.AttachmentData import AttachmentData
from dataclasses import dataclass


@dataclass
class TicketData:
    id: int
    author_tg_id: int
    created_at: int
    status: int
    review_message: str
    ticket_text: str
    attachments: List[AttachmentData]
    is_paper_included: bool
