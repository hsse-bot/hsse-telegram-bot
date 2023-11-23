from sqlalchemy import BigInteger, PickleType
from material_help_service.data.db.Base import Base


class AttachmentData(Base):
    __tablename__ = "attachment_data"

    id: BigInteger
    data: PickleType
