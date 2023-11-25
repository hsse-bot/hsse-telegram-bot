from datetime import datetime
from typing import List

from material_help_service.data.db.entities.Ticket import Ticket
from material_help_service.data.db.entities.TicketAttachment import TicketAttachment
from material_help_service.helpers.BaseTicketBuilder import BaseTicketBuilder


class TicketBuilder(BaseTicketBuilder):

    def __init__(self):
        self.author_tg_id_: int = 0
        self.created_at_ = None
        self.text_: str = ""
        self.attachments_: List[TicketAttachment] = []

    def with_author(self, tg_id: int):
        self.author_tg_id_ = tg_id
        return self

    def with_timestamp(self, time: datetime):
        self.created_at_ = time
        return self

    def with_text(self, txt: str):
        self.text_ = txt
        return self

    def with_attachment(self, mime_type: str, path: str):
        self.attachments_.append(TicketAttachment(mime_type=mime_type, path=path))
        return self

    def build(self) -> Ticket:
        ticket = Ticket()
        ticket.author_tg_id = self.author_tg_id_
        ticket.created_at = self.created_at_
        ticket.ticket_text = self.text_
        ticket.attachments = self.attachments_
        return ticket
