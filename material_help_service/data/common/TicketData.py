from typing import List
from material_help_service.data.db.Base import Base
from material_help_service.data.common.AttachmentData import AttachmentData


class TicketData(Base):
    __tablename__ = "ticket_data"

    id: int
    author_th_id: int
    created_at: int
    review_message: str
    ticket_text: str
    attachments: List[AttachmentData]
    is_paper_included: bool
