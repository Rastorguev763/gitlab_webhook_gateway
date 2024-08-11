import logging
from datetime import datetime, timedelta, timezone

from colorlog import ColoredFormatter
from pythonjsonlogger import jsonlogger

from .settings import settings

logger = logging.getLogger()


# Определяем свой форматтер, наследуясь от jsonlogger.JsonFormatter
class CustomTextFormatter(jsonlogger.JsonFormatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now(timezone(timedelta(hours=3))).strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
        }
        return f"""{log_record["timestamp"]} - {log_record["level"]}:
        {log_record["message"]} [module: {log_record["module"]} - func: {log_record["funcName"]}]"""


# Используем свой форматтер для обработчика логов
formatter = CustomTextFormatter(json_ensure_ascii=False)

# Добавляем обработчик для вывода в консоль
color_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s%(reset)s: %(message)s [%(module)s %(funcName)s]",
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(color_formatter)
logger.addHandler(stream_handler)

logger.setLevel(settings.LOGGING_LEVEL)

# Проверяем, установлена ли переменная окружения LOG_TO_FILE
if settings.LOG_TO_FILE:
    # Добавляем обработчик для записи в файл
    file_handler = logging.FileHandler(settings.log_file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
