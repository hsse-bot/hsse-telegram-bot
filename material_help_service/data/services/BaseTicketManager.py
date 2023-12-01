from abc import ABC, abstractmethod

from typing import Optional, List, NoReturn
from material_help_service.data.db.entities.Ticket import Ticket
from material_help_service.helpers.BaseTicketBuilder import BaseTicketBuilder


class BaseTicketManager(ABC):

    @abstractmethod
    def create_ticket(self, builder: BaseTicketBuilder) -> Ticket:
        pass

    @abstractmethod
    def edit_ticket(self, ticket_id: int, builder: BaseTicketBuilder) -> NoReturn:
        pass

    @abstractmethod
    def approve_ticket(self, ticket_id: int) -> NoReturn:
        pass

    @abstractmethod
    def deny_ticket(self, ticket_id: int) -> NoReturn:
        pass

    @abstractmethod
    def request_changes_for_ticket(self, ticket_id: int, msg: Optional[str]) -> NoReturn:
        pass

    @abstractmethod
    def delete_ticket(self, ticket_id: int) -> NoReturn:
        pass

    @abstractmethod
    def get_ticket(self, ticket_id: int) -> Ticket:
        pass

    @abstractmethod
    def get_tickets(self, is_active: bool, page_number: int, author_id: int) -> List[Ticket]:
        pass

    @abstractmethod
    def set_include_paper_status(self, ticket_id: int, is_paper_included: bool) -> NoReturn:
        pass
