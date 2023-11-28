import abc

from typing import Optional, List, NoReturn
from material_help_service.data.db.entities.Ticket import Ticket
from material_help_service.helpers.BaseTicketBuilder import BaseTicketBuilder


class BaseTicketManager(abc.ABC):

    @abc.abstractmethod
    def create_ticket(self, builder: BaseTicketBuilder) -> Ticket:
        pass

    @abc.abstractmethod
    def edit_ticket(self, ticket_id: int, builder: BaseTicketBuilder) -> NoReturn:
        pass

    @abc.abstractmethod
    def approve_ticket(self, ticket_id: int) -> NoReturn:
        pass

    @abc.abstractmethod
    def deny_ticket(self, ticket_id: int) -> NoReturn:
        pass

    @abc.abstractmethod
    def request_changes_for_ticket(self, ticket_id: int, msg: Optional[str]) -> NoReturn:
        pass

    @abc.abstractmethod
    def delete_ticket(self, ticket_id: int) -> NoReturn:
        pass

    @abc.abstractmethod
    def get_ticket(self, ticket_id: int) -> Ticket:
        pass

    @abc.abstractmethod
    def get_tickets(self, is_active: bool, page_number: int, author_id: int) -> List[Ticket]:
        pass

    @abc.abstractmethod
    def set_include_paper_status(self, ticket_id: int, is_paper_included: bool) -> NoReturn:
        pass
