from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Message(Base):
    __tablename__ = "messages"

    telegram_id: Mapped[int] = mapped_column(nullable=False)
    tread: Mapped[int] = mapped_column(nullable=True)
    caht_id: Mapped[int] = mapped_column(nullable=False)
    message_id: Mapped[int] = mapped_column(nullable=False)
    merge_request_id: Mapped[int] = mapped_column(nullable=False)
    action_merge_request: Mapped[str] = mapped_column(nullable=True)
    status_merge_request: Mapped[str] = mapped_column(nullable=True)
    created_at_merge_request: Mapped[datetime] = mapped_column(nullable=True)
    updated_at_merge_request: Mapped[datetime] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return "<Message for {tg_id} merge_request_id: {mr_id}, sataus: {st_mr}, action: {act_mr}>".format(
            tg_id=self.telegram_id,
            mr_id=self.merge_request_id,
            act_mr=self.action_merge_request,
            st_mr=self.status_merge_request,
        )
