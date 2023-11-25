from material_help_service.data.db.entities.Ticket import Ticket


class BaseTicketBuilder:
    def build(self) -> Ticket:
        pass
