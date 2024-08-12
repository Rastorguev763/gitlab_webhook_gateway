import uuid
from typing import Annotated
from sqlalchemy import text as text_
from datetime import datetime, timezone

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

uuid_pk = Annotated[
    uuid.UUID,
    mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
]
str_255 = Annotated[str, 255]


# Базовый класс для моделей
class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid_pk]
    created_at: Mapped[datetime] = mapped_column(server_default=text_("TIMEZONE('utc', now())"),
                                                 onupdate=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(server_default=text_("TIMEZONE('utc', now())"),
                                                 onupdate=datetime.now(timezone.utc))
    type_annotation_map = {str_255: String(255)}
