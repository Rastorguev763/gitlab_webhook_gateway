import os

from pydantic import Field
from pydantic_settings import BaseSettings


class Setting(BaseSettings):

    # Базовые настройки проекта
    MODE: str = Field(default="DEV", alias="MODE")
    PROJECT_NAME: str = Field(default="Gitlab gateway", alias="PROJECT_NAME")
    TYPING: bool = False

    # Настройки базы данных SQLite
    DABABASE_NAME: str = Field(default="GitlabGeteway", alias="DABABASE_NAME")

    # Настройки GitLab репозитория
    PRIVATE_TOKEN: str = Field(default="", alias="PRIVATE_TOKEN", required=True)
    URL_GITLAB: str = Field(default="https://gitlab.com/", alias="URL_GITLAB")

    # Настройки телеграм бота
    BOT_TOKEN: str = Field(default=None, alias="BOT_TOKEN", required=True)
    SERVER_URL: str = Field(default="", alias="SERVER_URL")
    CHAT_ID: str = Field(default="", alias="CHAT_ID", required=True)
    THREAD_ID: int = Field(default=0, alias="THREAD_ID")

    # Настройки логирования
    LOGGING_LEVEL: str = Field(default="DEBUG", alias="LOGGING_LEVEL")
    LOG_TO_FILE: bool = Field(default=False, alias="LOG_TO_FILE")
    BASE_DIR_LOGS: str = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    LOG_DIRECTORY: str = Field(default=os.path.join(BASE_DIR_LOGS, "logs"), alias="LOG_DIRECTORY")

    @property
    def log_file_path(self):
        os.makedirs(settings.LOG_DIRECTORY, exist_ok=True)

        return os.path.join(self.LOG_DIRECTORY, "debug.log")

    @property
    def database_url_async(self):
        return "sqlite+aiosqlite:///./{name}.db".format(
            name=self.DABABASE_NAME,
        )

    @property
    def database_url_sync(self):
        return "sqlite:///./{name}.db".format(
            name=self.DABABASE_NAME,
        )


settings = Setting()
