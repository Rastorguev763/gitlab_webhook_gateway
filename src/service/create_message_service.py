from functools import lru_cache
from sqlalchemy import select

from fastapi import Depends

from src.core.settings import settings
from src.schemas.merge_request_schemas import WebhookPayload
from src.db.aiosqlite import get_async_session
from src.service.base_service import BaseService
from src.utils.bot import send_telegram_message
from src.utils.gitlab_connect import gitlab_connect
from src.models.message import Message
from sqlalchemy.ext.asyncio import AsyncSession


class CreateMessageService(BaseService):
    model = Message

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_message_merge_request(self, data: WebhookPayload) -> str:
        text = (
            f"<b>📬 <a href='{data.object_attributes.url}'>"
            f"Запрос на слияние № {data.object_attributes.iid}</a></b>\n\n"
            f"<b>✏️ Действие:</b> {data.object_attributes.action}\n"
            f"<b>🗂 Проект:</b> {data.project.name}\n"
            f"<b>🌳 Ветка:</b> {data.object_attributes.source_branch} ➜ "
            f"{data.object_attributes.target_branch}\n"
            f"<b>👤 Создатель события:</b> {data.user.name}\n"
            f"<b>💬 Последний коммит:</b> {data.object_attributes.last_commit.message}\n"
            f"<b>📅 Дата:</b> {data.object_attributes.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        match data.object_attributes.merge_status:
            case "can_be_merged":
                text += "<b>✅ Конфилктов слияния нет.</b>"
            case _:
                text += "<b>❌ Есть конфликты слияния!! 😱</b>"
        commits = gitlab_connect.get_commits(
            project=gitlab_connect.get_projects(project_id=data.project.id),
            branch_name=data.object_attributes.source_branch,
        )
        text += "\n------------------\n<b>⚙️ ИЗМЕНЕНИЯ В КОДЕ ⚙️</b>\n------------------\n"
        for commit in commits:
            text += f"<b>{commit.author_name}</b> - {commit.message}"
        msg = await send_telegram_message(chat_id=settings.CHAT_ID, message=text)
        # print(f"\n\n{msg}\n\n")
        message = Message(
            telegram_id=settings.BOT_TOKEN.split(":")[0],
            tread=settings.THREAD_ID,
            caht_id=settings.CHAT_ID,
            message_id=1,
            merge_request_id=data.object_attributes.iid,
            action_merge_request=data.object_attributes.action,
            # status_merge_request =
            # created_at_merge_request=data.object_attributes.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            #                     updated_at_merge_request =
        )
        self._session.add(message)
        await self._session.commit()
        return "success"

    async def get_message_by_tg_id(
        self,
        message_id: int,
        merge_request_id: int,
    ) -> Message:
        message_result = await self._session.execute(
            select(Message)
            .filter(Message.message_id == message_id)
            .filter(Message.merge_request_id == merge_request_id)
        )
        message = message_result.scalar_one_or_none()
        return message


@lru_cache()
def get_create_message_service(
    session: AsyncSession = Depends(get_async_session),
) -> CreateMessageService:
    return CreateMessageService(session)
