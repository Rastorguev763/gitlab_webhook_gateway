from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    _session: AsyncSession
    model: Any
    _table_name: str

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session
