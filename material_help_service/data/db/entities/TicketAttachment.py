from sqlalchemy import BigInteger, String, LargeBinary
from sqlalchemy.orm import Mapped
from Ticket import Ticket
from material_help_service.data.db.Base import Base


class TicketAttachment(Base):
    __tablename__ = "ticket_attachment"

    id: Mapped[BigInteger]
    mime_type: Mapped[String]
    content: Mapped[LargeBinary]
    ticket_id: Mapped[BigInteger]
    ticket: Mapped[Ticket]
