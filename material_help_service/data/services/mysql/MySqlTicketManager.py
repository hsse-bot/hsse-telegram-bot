import os
from typing import Optional, List, NoReturn
from data.db.entities.Ticket import Ticket
from data.services.BaseTicketManager import BaseTicketManager
from helpers.BaseTicketBuilder import BaseTicketBuilder

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session


class MySqlTicketManager(BaseTicketManager):
    _engine = create_engine(os.environ.get("MY_SQL_CONNECTION_STRING"), echo=True)
    _APPROVED: int = 1
    _NEED_CHANGES: int = 2
    _DENIED: int = 3

    def create_ticket(self, builder: BaseTicketBuilder) -> Ticket:
        with Session(self._engine) as session:
            ticket = builder.build()
            session.add(ticket)
            session.commit()
            return ticket

    def edit_ticket(self, ticket_id: int, builder: BaseTicketBuilder) -> NoReturn:
        with Session(self._engine) as session:
            stmt = select(Ticket).where(Ticket.id == ticket_id)
            ticket = session.scalars(stmt).one()
            new_ticket = builder.build()

            ticket.id = new_ticket.id
            ticket.author_tg_id = new_ticket.author_tg_id
            ticket.created_at = new_ticket.created_at
            ticket.status = new_ticket.status
            ticket.review_message = new_ticket.review_message
            ticket.ticket_text = new_ticket.ticket_text
            ticket.attachments = new_ticket.attachments
            ticket.is_paper_included = new_ticket.is_paper_included
            session.commit()

    def approve_ticket(self, ticket_id: int) -> NoReturn:
        with Session(self._engine) as session:
            stmt = select(Ticket).where(Ticket.id == ticket_id)
            ticket = session.scalars(stmt).one()
            ticket.status = self._APPROVED
            session.commit()

    def deny_ticket(self, ticket_id: int) -> NoReturn:
        with Session(self._engine) as session:
            stmt = select(Ticket).where(Ticket.id == ticket_id)
            ticket = session.scalars(stmt).one()
            ticket.status = self._DENIED
            session.commit()

    def request_changes_for_ticket(self, ticket_id: int, msg: Optional[str]) -> NoReturn:
        with Session(self._engine) as session:
            stmt = select(Ticket).where(Ticket.id == ticket_id)
            ticket = session.scalars(stmt).one()
            ticket.status = self._NEED_CHANGES
            ticket.review_message = msg
            session.commit()

    def delete_ticket(self, ticket_id: int) -> NoReturn:
        with Session(self._engine) as session:
            stmt = select(Ticket).where(Ticket.id == ticket_id)
            ticket = session.scalars(stmt).one()
            session.delete(ticket)
            session.commit()

    def get_ticket(self, ticket_id: int) -> Ticket:
        with Session(self._engine) as session:
            stmt = select(Ticket).where(Ticket.id == ticket_id)
            ticket = session.scalars(stmt).one()
            return ticket

    def get_tickets(self, is_active: bool, page_number: int, author_id: int) -> List[Ticket]:
        with Session(self._engine) as session:
            stmt = select(Ticket).where(Ticket.status == is_active, Ticket.author_tg_id == author_id)
            tickets = session.scalars(stmt).all()
            return [x for x in tickets]

    def set_include_paper_status(self, ticket_id: int, is_paper_included: bool) -> NoReturn:
        with Session(self._engine) as session:
            stmt = select(Ticket).where(Ticket.id == ticket_id)
            ticket = session.scalars(stmt).one()
            ticket.is_paper_included = is_paper_included
            session.commit()
