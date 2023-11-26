from datetime import datetime
from typing import List

from material_help_service.data.db.entities.Ticket import Ticket
from material_help_service.data.db.entities.TicketAttachment import TicketAttachment
from material_help_service.helpers.BaseTicketBuilder import BaseTicketBuilder


class TicketBuilder(BaseTicketBuilder):
    def __init__(self):
        self._author_tg_id: int = 0
        self._created_at = None
        self._text: str = ""
        self._attachments: List[TicketAttachment] = []

    def with_author(self, tg_id: int):
        self._author_tg_id = tg_id
        return self

    def with_timestamp(self, time: datetime):
        self._created_at = time
        return self

    def with_text(self, txt: str):
        self._text = txt
        return self

    def with_attachment(self, mime_type: str, path: str):
        self._attachments.append(TicketAttachment(mime_type=mime_type, path=path))
        return self

    def build(self) -> Ticket:
        ticket = Ticket()
        if self._author_tg_id == 0:
            raise Exception('Telegram ID was not given')
        ticket.author_tg_id = self._author_tg_id

        if ticket.created_at is None:
            raise Exception('Creation time was not given')
        ticket.created_at = self._created_at

        if ticket.ticket_text == "":
            raise Exception('Ticket text was not given')
        ticket.ticket_text = self._text

        if not ticket.attachments:
            raise Exception('Attachments were not given')
        ticket.attachments = self._attachments
        return ticket
