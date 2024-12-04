from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import logger
from src.core.settings import settings
from src.db.aiosqlite import get_async_session
from src.exceptions.base_exceptions import ObjectNotFound
from src.models.message import Message, MessagePipeline
from src.schemas.merge_request_schemas import WebhookPayload
from src.schemas.pipeline_schemas import PipelineSchemas
from src.service.base_service import BaseService
from src.utils.bot import send_message_reaction, send_telegram_message, update_message_text
from src.utils.gitlab_connect import gitlab_connect


class CreateMessageService(BaseService):
    model: Message = Message
    pipeline_model = MessagePipeline

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_message_merge_request(self, data: WebhookPayload) -> str:

        message: Message = self.model(
            telegram_id=settings.BOT_TOKEN.split(":")[0],
            tread=settings.THREAD_ID,
            chat_id=settings.CHAT_ID,
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
                # await send_telegram_message(
                #     chat_id=settings.CHAT_ID,
                #     message=f"Смержено! 🥳👏🏻\nВсе валить на <b>{data.user.name}</b> ",
                #     reply_to_message_id=one_message.message_id,
                #     thread_id=settings.THREAD_ID,
                # )
                await update_message_text(
                        chat_id=settings.CHAT_ID,
                        message_id=one_message.message_id,
                        new_text=(
                            await self.create_message_text(data=data)
                            + f"\nСмержено! 🥳👏🏻\nВсе валить на <b>{data.user.name}</b>"
                        ),
                    )
                await send_message_reaction(
                    chat_id=settings.CHAT_ID,
                    message_id=one_message.message_id,
                    reaction="🎉",
                )
            case "opened":
                if data.object_attributes.action == "approved":
                    one_message = await self.get_message_by_mr_id(
                        merge_request_id=data.object_attributes.iid, project_name=data.project.name
                    )
                    await update_message_text(
                        chat_id=settings.CHAT_ID,
                        message_id=one_message.message_id,
                        new_text=(
                            await self.create_message_text(data=data)
                            + f"\n<b>👤 {data.user.name}</b> за качество отвечает. Апрувнуто! 💪🏻"
                        ),
                    )
                elif data.object_attributes.action == "reopen":
                    one_message = await self.get_message_by_mr_id(
                        merge_request_id=data.object_attributes.iid, project_name=data.project.name
                    )
                    await update_message_text(
                        chat_id=settings.CHAT_ID,
                        message_id=one_message.message_id,
                        new_text=(
                            await self.create_message_text(data=data)
                            + f"\n<b>👤 {data.user.name}</b> сново открыл слияние! 👋🏻"
                        ),
                    )
                elif data.object_attributes.action == "unapproved":
                    one_message = await self.get_message_by_mr_id(
                        merge_request_id=data.object_attributes.iid, project_name=data.project.name
                    )
                    await update_message_text(
                        chat_id=settings.CHAT_ID,
                        message_id=one_message.message_id,
                        new_text=(
                            await self.create_message_text(data=data)
                            + f"\n<b>👤 {data.user.name}</b> апрув отозвал! 👎🏻"
                        ),
                    )
                elif data.object_attributes.action == "update":
                    one_message = await self.get_message_by_mr_id(
                        merge_request_id=data.object_attributes.iid, project_name=data.project.name
                    )
                    await update_message_text(
                        chat_id=settings.CHAT_ID,
                        message_id=one_message.message_id,
                        new_text=await self.create_message_text(data=data),
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
                await update_message_text(
                        chat_id=settings.CHAT_ID,
                        message_id=one_message.message_id,
                        new_text=(
                            await self.create_message_text(data=data)
                            + f"\n<b>👤 {data.user.name}</b> закрыл слияние! 😭"
                        ),
                    )
                await send_message_reaction(
                    chat_id=settings.CHAT_ID,
                    message_id=one_message.message_id,
                    reaction="😭",
                )
            case "update":
                one_message = await self.get_message_by_mr_id(
                    merge_request_id=data.object_attributes.iid, project_name=data.project.name
                )
                await update_message_text(
                        chat_id=settings.CHAT_ID,
                        message_id=one_message.message_id,
                        new_text=await self.create_message_text(data=data),
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

    async def get_message_by_ppln_id(
        self,
        project_name: str,
        pipeline_id: int,
    ) -> MessagePipeline:
        try:
            message_result = await self._session.execute(
                select(MessagePipeline)
                .filter(MessagePipeline.project_name == project_name)
                .filter(MessagePipeline.pipeline_id == pipeline_id)
            )
            message = message_result.scalar_one_or_none()
            if not message:
                logger.error("Message info from pipeline request not found")
                raise ObjectNotFound(detail="Message info from pipeline request not found")
        except Exception as e:
            logger.error(f"Error get info message from pipeline request in database: {e}")
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
                text += "<b>✅ Конфликтов слияния нет.</b>"
            case "checking":
                text += "<b>✅ Конфликтов слияния нет.</b>"
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

    async def create_message_pipeline_request(self, data: PipelineSchemas):
        message_pipeline = self.pipeline_model(
            telegram_id=settings.BOT_TOKEN.split(":")[0],
            tread=settings.THREAD_ID,
            chat_id=settings.CHAT_ID,
            pipeline_id=data.object_attributes.iid,
            project_name=data.project.name,
            status_pipeline=data.object_attributes.status,
        )

        text = (
            f"<b>📬 <a href='{data.object_attributes.url}'>"
            f"Новая сборочная линия: № {data.object_attributes.id}</a></b>\n\n"
            f"<b>🗂 Проект:</b> {data.project.name}\n"
            f"<b>🌳 Ветка:</b> {data.object_attributes.ref}\n"
            f"<b>👤 Создатель события:</b> {data.user.name}\n"
            f"<b>📅 Дата:</b> {data.object_attributes.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        )
        match message_pipeline.status_pipeline:
            case "pending":
                msg = await send_telegram_message(
                    chat_id=settings.CHAT_ID,
                    message=text,
                    thread_id=settings.THREAD_ID,
                )

                message_pipeline.message_id = msg.message_id

                self._session.add(message_pipeline)
                await self._session.commit()
            case "running":
                one_message = await self.get_message_by_ppln_id(
                    pipeline_id=data.object_attributes.iid, project_name=data.project.name
                )
                if (
                    len(data.object_attributes.stages) == 1
                    and "test" in data.object_attributes.stages
                ):
                    new_text = text + "🚀 Запущены тесты...\n"

                else:
                    new_text = text + "🚀 Запущен деплой приложения...\n"
                await update_message_text(
                    chat_id=settings.CHAT_ID,
                    message_id=one_message.message_id,
                    new_text=new_text,
                )
                await send_message_reaction(
                    chat_id=settings.CHAT_ID,
                    message_id=one_message.message_id,
                    reaction="👀",
                )
            case "success":
                one_message = await self.get_message_by_ppln_id(
                    pipeline_id=data.object_attributes.iid, project_name=data.project.name
                )
                if (
                    len(data.object_attributes.stages) == 1
                    and "test" in data.object_attributes.stages
                ):
                    new_text = text + "✅ Тесты успешно прошли! 🥳\n"
                else:
                    new_text = text + "✅ Деплой закончился успешно.\nПриложение развернуто! 🥳\n"
                await update_message_text(
                    chat_id=settings.CHAT_ID,
                    message_id=one_message.message_id,
                    new_text=new_text,
                )
                await send_message_reaction(
                    chat_id=settings.CHAT_ID,
                    message_id=one_message.message_id,
                    reaction="👍",
                )
            case "failed":
                one_message = await self.get_message_by_ppln_id(
                    pipeline_id=data.object_attributes.iid, project_name=data.project.name
                )
                if (
                    len(data.object_attributes.stages) == 1
                    and "test" in data.object_attributes.stages
                ):
                    new_text = text + "❌ Тесты не прошли! 😱\nПроверь логи сборки."
                else:
                    new_text = text + "❌ Деплой закончилась провалом! 😱\nПроверь логи сборки."
                await update_message_text(
                    chat_id=settings.CHAT_ID,
                    message_id=one_message.message_id,
                    new_text=new_text,
                )
                await send_message_reaction(
                    chat_id=settings.CHAT_ID,
                    message_id=one_message.message_id,
                    reaction="👎",
                )
            case "canceled":
                one_message = await self.get_message_by_ppln_id(
                    pipeline_id=data.object_attributes.iid, project_name=data.project.name
                )
                new_text = text + "❌ Сборочная линия отменена!"
                await update_message_text(
                    chat_id=settings.CHAT_ID,
                    message_id=one_message.message_id,
                    new_text=new_text,
                )
                await send_message_reaction(
                    chat_id=settings.CHAT_ID,
                    message_id=one_message.message_id,
                    reaction="😭",
                )


@lru_cache()
def get_create_message_service(
    session: AsyncSession = Depends(get_async_session),
) -> CreateMessageService:
    return CreateMessageService(session)
