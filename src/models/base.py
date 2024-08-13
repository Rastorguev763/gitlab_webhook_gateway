import uuid
from datetime import datetime, timezone
from typing import Annotated

from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

uuid_pk = Annotated[
    uuid.UUID,
    mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
]
str_255 = Annotated[str, 255]


# Базовый класс для моделей
class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid_pk]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.datetime("now", "utc"), onupdate=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.datetime("now", "utc"), onupdate=datetime.now(timezone.utc)
    )
    type_annotation_map = {str_255: String(255)}
