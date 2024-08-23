from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Message(Base):
    __tablename__ = "messages"

    telegram_id: Mapped[int] = mapped_column(nullable=False)
    tread: Mapped[int] = mapped_column(nullable=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    message_id: Mapped[int] = mapped_column(nullable=False)
    merge_request_id: Mapped[int] = mapped_column(nullable=False)
    project_name: Mapped[str] = mapped_column(nullable=False)
    action_merge_request: Mapped[str] = mapped_column(nullable=True)
    status_merge_request: Mapped[str] = mapped_column(nullable=True)
    created_at_merge_request: Mapped[datetime] = mapped_column(nullable=True)
    updated_at_merge_request: Mapped[datetime] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return "<Message for {tg_id} merge_request_id: {mr_id}, status: {st_mr}, action: {act_mr}>".format(
            tg_id=self.telegram_id,
            mr_id=self.merge_request_id,
            act_mr=self.action_merge_request,
            st_mr=self.status_merge_request,
        )


class MessagePipeline(Base):
    __tablename__ = "messages_pipelines"

    telegram_id: Mapped[int] = mapped_column(nullable=False)
    tread: Mapped[int] = mapped_column(nullable=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    message_id: Mapped[int] = mapped_column(nullable=False)
    pipeline_id: Mapped[int] = mapped_column(nullable=False)
    project_name: Mapped[str] = mapped_column(nullable=False)
    action_pipeline: Mapped[str] = mapped_column(nullable=True)
    status_pipeline: Mapped[str] = mapped_column(nullable=True)
    created_at_pipeline: Mapped[datetime] = mapped_column(nullable=True)
    updated_at_pipeline: Mapped[datetime] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return "<Message for {tg_id} pipeline_id: {ppln_id}, status: {st_ppln}, action: {act_ppln}>".format(
            tg_id=self.telegram_id,
            ppln_id=self.pipeline_id,
            act_ppln=self.action_pipeline,
            st_ppln=self.status_pipeline,
        )
