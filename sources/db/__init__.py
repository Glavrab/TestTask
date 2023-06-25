from typing import Any

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from sources.shared.constants import project_settings

async_engine = create_async_engine(project_settings.db_uri)


def generate_async_session() -> async_sessionmaker[AsyncSession | Any] | async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        future=True
    )
