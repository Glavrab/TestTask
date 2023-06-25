from typing import Optional, cast

from sqlalchemy import Integer, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sources.schemas.test_task_types import Balance, UserId
from sources.shared.constants import BASE_USER_BALANCE


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[int] = mapped_column(Integer, default=BASE_USER_BALANCE, nullable=False)

    @classmethod
    async def get_user_id(cls, user_id: UserId, session: AsyncSession) -> Optional['User']:
        query = select(cls).where(cls.id == user_id)
        return await session.scalar(query)

    @classmethod
    async def get_multiple_users_by_ids(cls, user_ids: list[UserId], session: AsyncSession) -> list[Optional['User']]:
        query = select(cls).where(cls.id.in_(user_ids))
        results = await session.scalars(query)
        results = cast(list[User | None], results)
        return results

    @classmethod
    async def add_new_user(cls, session: AsyncSession) -> UserId:
        query = insert(cls).values({cls.balance: BASE_USER_BALANCE}).returning(cls.id)
        new_user_id = await session.scalar(query)
        await session.commit()
        return new_user_id

    @classmethod
    async def process_money_transfer(
            cls,
            amount_of_money_to_transfer: Balance,
            sender_id: UserId,
            current_sender_balance: Balance,
            recipient_id: UserId,
            session: AsyncSession
    ) -> None:
        decrease_sender_balance = update(
            cls
        ).where(
            cls.id == sender_id
        ).values(
            balance=current_sender_balance - amount_of_money_to_transfer
        )
        await session.execute(decrease_sender_balance)
        increase_recipient_balance = update(
            cls
        ).where(
            cls.id == recipient_id
        ).values(
            balance=cls.balance + amount_of_money_to_transfer
        )
        await session.execute(increase_recipient_balance)
        await session.commit()
