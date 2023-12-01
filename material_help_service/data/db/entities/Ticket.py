from typing import Optional, List

from sqlalchemy import BigInteger, String, DateTime, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from TicketAttachment import TicketAttachment
from material_help_service.data.db.Base import Base


class Ticket(Base):
    __tablename__ = "ticket"

    id: Mapped[BigInteger] = mapped_column(primary_key=True)
    author_tg_id: Mapped[BigInteger]
    created_at: Mapped[DateTime]
    status: Mapped[SmallInteger]
    review_message: Mapped[Optional[str]]
    ticket_text: Mapped[String]
    attachments: Mapped[List[TicketAttachment]] = relationship(back_populates="ticket", cascade="all, delete-orphan")
    is_paper_included: Mapped[bool]
