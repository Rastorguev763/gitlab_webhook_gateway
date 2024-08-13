from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import logger
from src.core.settings import settings
from src.db.aiosqlite import get_async_session
from src.exceptions.base_exceptions import ObjectNotFound
from src.models.message import Message
from src.schemas.merge_request_schemas import WebhookPayload
from src.service.base_service import BaseService
from src.utils.bot import send_telegram_message
from src.utils.gitlab_connect import gitlab_connect


class CreateMessageService(BaseService):
    model = Message

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_message_merge_request(self, data: WebhookPayload) -> str:

        message = Message(
            telegram_id=settings.BOT_TOKEN.split(":")[0],
            tread=settings.THREAD_ID,
            caht_id=settings.CHAT_ID,
            merge_request_id=data.object_attributes.iid,
            project_name=data.project.name,
            action_merge_request=data.object_attributes.action,
            status_merge_request=data.object_attributes.state,
            # TODO: доделать время
            # created_at_merge_request=data.object_attributes.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            # updated_at_merge_request =
        )

        match message.status_merge_request:
            case "merged":
                one_message = await self.get_message_by_mr_id(
                    merge_request_id=data.object_attributes.iid, project_name=data.project.name
                )
                await send_telegram_message(
                    chat_id=settings.CHAT_ID,
                    message=f"Смержено! 🥳👏🏻\nВсе валить на <b>{data.user.name}</b> ",
                    reply_to_message_id=one_message.message_id,
                    thread_id=settings.THREAD_ID,
                )
            case "opened":
                if data.object_attributes.action == "approved":
                    one_message = await self.get_message_by_mr_id(
                        merge_request_id=data.object_attributes.iid, project_name=data.project.name
                    )
                    await send_telegram_message(
                        chat_id=settings.CHAT_ID,
                        message=f"<b>👤 {data.user.name}</b> за качество отвечает. Апрувнуто! 💪🏻",
                        reply_to_message_id=one_message.message_id,
                        thread_id=settings.THREAD_ID,
                    )
                elif data.object_attributes.action == "reopen":
                    one_message = await self.get_message_by_mr_id(
                        merge_request_id=data.object_attributes.iid, project_name=data.project.name
                    )
                    await send_telegram_message(
                        chat_id=settings.CHAT_ID,
                        message=f"<b>👤 {data.user.name}</b> сново открыл слияние! 👋🏻",
                        reply_to_message_id=one_message.message_id,
                        thread_id=settings.THREAD_ID,
                    )
                elif data.object_attributes.action == "unapproved":
                    one_message = await self.get_message_by_mr_id(
                        merge_request_id=data.object_attributes.iid, project_name=data.project.name
                    )
                    await send_telegram_message(
                        chat_id=settings.CHAT_ID,
                        message=f"<b>👤 {data.user.name}</b> апрув отозвал! 👎🏻",
                        reply_to_message_id=one_message.message_id,
                        thread_id=settings.THREAD_ID,
                    )
                else:
                    msg = await send_telegram_message(
                        thread_id=settings.THREAD_ID,
                        chat_id=settings.CHAT_ID,
                        message=await self.create_message_text(data=data),
                    )
                    message.message_id = msg.message_id

                    self._session.add(message)
                    await self._session.commit()
            case "closed":
                one_message = await self.get_message_by_mr_id(
                    merge_request_id=data.object_attributes.iid, project_name=data.project.name
                )
                await send_telegram_message(
                    chat_id=settings.CHAT_ID,
                    message=f"<b>👤 {data.user.name}</b> закрыл слияние! 😭",
                    reply_to_message_id=one_message.message_id,
                    thread_id=settings.THREAD_ID,
                )
        return "success"

    async def get_message_by_mr_id(
        self,
        project_name: str,
        merge_request_id: int,
    ) -> Message:
        try:
            message_result = await self._session.execute(
                select(Message)
                .filter(Message.project_name == project_name)
                .filter(Message.merge_request_id == merge_request_id)
            )
            message = message_result.scalar_one_or_none()
            if not message:
                logger.error("Message info from merge request not found")
                raise ObjectNotFound(detail="Message info from merge request not found")
        except Exception as e:
            logger.error(f"Error get info message from merge request in database: {e}")
        return message

    async def create_message_text(
        self,
        data: WebhookPayload,
    ) -> str:
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
                text += "<b>✅ Конфиликтов слияния нет.</b>"
            case "checking":
                text += "<b>✅ Конфиликтов слияния нет.</b>"
            case _:
                text += "<b>❌ Есть конфликты слияния!! 😱</b>"

        commits = await self.get_actual_commits(
            sourse_branch=data.object_attributes.source_branch,
            target_branch=data.object_attributes.target_branch,
            project_id=data.project.id,
        )

        text += "\n------------------\n<b>⚙️ ИЗМЕНЕНИЯ В КОДЕ ⚙️</b>\n------------------\n"
        for commit in commits:
            text += f"{commit}\n"

        return text

    async def get_actual_commits(
        self, sourse_branch: str, target_branch: str, project_id: int
    ) -> list:
        commits_source_branch = gitlab_connect.get_commits(
            project=gitlab_connect.get_projects(project_id=project_id),
            branch_name=sourse_branch,
        )
        commits_target_branch = gitlab_connect.get_commits(
            project=gitlab_connect.get_projects(project_id=project_id),
            branch_name=target_branch,
        )
        # Приводим сообщения коммитов к единому виду, включая имя автора, и собираем их в множества
        messages_source = {
            f"<b>{commit.author_name}</b> - {commit.message}".rstrip("\n")
            for commit in commits_source_branch
        }
        messages_target = {
            f"<b>{commit.author_name}</b> - {commit.message}".rstrip("\n")
            for commit in commits_target_branch
        }

        unique_to_source = messages_source - messages_target

        return unique_to_source


@lru_cache()
def get_create_message_service(
    session: AsyncSession = Depends(get_async_session),
) -> CreateMessageService:
    return CreateMessageService(session)
