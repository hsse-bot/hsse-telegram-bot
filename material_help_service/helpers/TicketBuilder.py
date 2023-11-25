from datetime import datetime
from typing import List

from material_help_service.data.db.entities.Ticket import Ticket
from material_help_service.data.db.entities.TicketAttachment import TicketAttachment
from material_help_service.helpers.BaseTicketBuilder import BaseTicketBuilder


class TicketBuilder(BaseTicketBuilder):
    created_at: datetime
    attachment: TicketAttachment
    author_tg_id: int
    text: str
    attachments: List[TicketAttachment]

    def with_author(self, tg_id: int):
        self.author_tg_id = tg_id

    def with_timestamp(self, time: datetime):
        self.created_at = time

    def with_text(self, txt: str):
        self.text = txt

    def with_attachment(self, mime_type: str, path: str):
        self.attachment.mime_type = mime_type
        self.attachment.path = path
        self.attachments.append(self.attachment)

    def build(self) -> Ticket:
        return Ticket(self)
