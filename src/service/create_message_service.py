from functools import lru_cache

from core.settings import settings
from schemas.merge_request_schemas import WebhookPayload
from utils.gitlab_connect import gitlab_connect
from utils.bot import send_telegram_message


class CreateMessage:

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
        await send_telegram_message(chat_id=settings.CHAT_ID, message=text)

        return "success"


@lru_cache()
def get_create_message_service() -> CreateMessage:
    return CreateMessage()
