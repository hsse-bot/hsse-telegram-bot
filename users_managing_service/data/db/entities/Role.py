from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from users_managing_service.data.db import Base
from sqlalchemy import String


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(32))
