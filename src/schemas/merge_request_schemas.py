from datetime import datetime
from typing import List, Optional

import pytz
from pydantic import BaseModel, field_validator


# Определяем модели для данных вебхука merge request
class Author(BaseModel):
    name: str
    email: str


class Commit(BaseModel):
    id: str
    message: str
    title: str
    timestamp: str
    url: str
    author: Author


class Project(BaseModel):
    id: int
    name: str
    description: Optional[str]
    web_url: str
    avatar_url: Optional[str]
    git_ssh_url: str
    git_http_url: str
    namespace: str
    visibility_level: int
    path_with_namespace: str
    default_branch: str
    ci_config_path: Optional[str]
    homepage: str
    url: str
    ssh_url: str
    http_url: str


class Repository(BaseModel):
    name: str
    url: str
    description: Optional[str]
    homepage: str


class User(BaseModel):
    id: int
    name: str
    username: str


class ObjectAttributes(BaseModel):
    iid: int  # ID merge request
    merge_status: str
    source_branch: str
    target_branch: str
    last_commit: Commit
    source: Project
    state: str
    target: Project
    url: str
    created_at: Optional[datetime] = None
    action: Optional[str] = None

    @field_validator("created_at", mode="before")
    def parse_datetime(cls, value):
        if isinstance(value, datetime):
            return value

        # Преобразование из строки в datetime
        if isinstance(value, str):
            # Обработка формата `2024-08-09 13:08:01 UTC`
            timezone = pytz.timezone("Europe/Moscow")
            if "UTC" in value:
                value = value.replace(" UTC", "Z")
                try:
                    # Преобразование времени в UTC+3
                    return datetime.fromisoformat(value).astimezone(timezone)
                except ValueError:
                    raise ValueError(f"Invalid datetime format: {value}")
            # Обработка формата `2024-08-09T13:08:01.152Z`
            try:
                # Преобразование времени в UTC+3
                return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone)
            except ValueError:
                raise ValueError(f"Invalid datetime format: {value}")

        raise TypeError("Invalid type. Expected a datetime string or datetime object.")


class WebhookPayload(BaseModel):
    object_kind: str
    event_type: str
    user: User
    project: Project
    object_attributes: ObjectAttributes
    repository: Repository
    assignees: List[User]
