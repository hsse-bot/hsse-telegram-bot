from sqlalchemy import BigInteger, String, LargeBinary, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Ticket import Ticket
from data.db.Base import Base


class TicketAttachment(Base):
    __tablename__ = "ticket_attachment"

    id: Mapped[BigInteger] = mapped_column(primary_key=True)
    filename: Mapped[String]
    mime_type: Mapped[String]
    content: Mapped[LargeBinary]
    ticket_id: Mapped[BigInteger] = mapped_column(ForeignKey("ticket.id"))
    ticket: Mapped[Ticket] = relationship(back_populates="attachments")
