from typing import List, Optional
from pydantic import BaseModel, field_validator
from datetime import datetime

import pytz


class Variable(BaseModel):
    key: str
    value: str


class ArtifactFile(BaseModel):
    filename: Optional[str]
    size: Optional[int]


class Environment(BaseModel):
    name: str
    action: str
    deployment_tier: str


class User(BaseModel):
    id: int
    name: str
    username: str


class Build(BaseModel):
    id: int
    stage: str
    name: str
    status: str
    created_at: datetime
    # started_at: Optional[datetime]
    # finished_at: Optional[datetime]
    duration: Optional[float]
    queued_duration: Optional[float]
    failure_reason: Optional[str]
    when: str
    manual: bool
    allow_failure: bool
    user: User
    runner: Optional[dict]
    artifacts_file: ArtifactFile
    environment: Optional[Environment]

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


class CommitAuthor(BaseModel):
    name: str
    email: str


class Commit(BaseModel):
    id: str
    message: str
    title: str
    timestamp: datetime
    url: str
    author: CommitAuthor


class Project(BaseModel):
    id: int
    name: str
    namespace: str
    path_with_namespace: str
    default_branch: str
    ci_config_path: Optional[str]


class ObjectAttributes(BaseModel):
    id: int
    iid: int
    name: Optional[str]
    ref: str
    tag: bool
    source: str
    status: str
    detailed_status: str
    stages: List[str]
    created_at: datetime
    url: str

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


class PipelineSchemas(BaseModel):
    object_kind: str
    object_attributes: ObjectAttributes
    merge_request: Optional[dict]
    user: User
    project: Project
    commit: Commit
    builds: List[Build]
