import os
from typing import Optional, List, NoReturn
from material_help_service.data.db.entities.Ticket import Ticket
from material_help_service.data.services.BaseTicketManager import BaseTicketManager
from material_help_service.helpers.BaseTicketBuilder import BaseTicketBuilder

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session


class MySqlTicketManager(BaseTicketManager):
    _engine = create_engine(os.environ.get("MY_SQL_CONNECTION_STRING"), echo=True)

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
            # Все поля поодельности присвоить

    def approve_ticket(self, ticket_id: int) -> NoReturn:
        with Session(self._engine) as session:
            stmt = select(Ticket).where(Ticket.id == ticket_id)
            ticket = session.scalars(stmt).one()
            ticket.status = 1
            session.commit()

    def deny_ticket(self, ticket_id: int) -> NoReturn:
        with Session(self._engine) as session:
            stmt = select(Ticket).where(Ticket.id == ticket_id)
            ticket = session.scalars(stmt).one()
            ticket.status = 3
            session.commit()

    def request_changes_for_ticket(self, ticket_id: int, msg: Optional[str]) -> NoReturn:
        with Session(self._engine) as session:
            stmt = select(Ticket).where(Ticket.id == ticket_id)
            ticket = session.scalars(stmt).one()
            ticket.status = 2
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
            tickets_list = [x for x in tickets]
            return tickets_list

    def set_include_paper_status(self, ticket_id: int, is_paper_included: bool) -> NoReturn:
        with Session(self._engine) as session:
            stmt = select(Ticket).where(Ticket.id == ticket_id)
            ticket = session.scalars(stmt).one()
            ticket.is_paper_included = is_paper_included
            session.commit()
