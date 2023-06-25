from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from sources.db import async_sessionmaker
from sources.db.dao import User
from sources.schemas.requests import MoneyTransferRequest
from sources.schemas.test_task_types import Balance, UserId
from sources.shared.exceptions import Conflict, ObjectNotFound


class UserModel:

    def __init__(self, user_dao: Type[User], session: async_sessionmaker[AsyncSession]) -> None:
        self._user_dao = user_dao
        self._session = session

    async def create_new_user(self) -> UserId:
        async with self._session() as session:
            return await self._user_dao.add_new_user(session)

    async def get_user_balance(self, user_id: UserId) -> Balance:
        async with self._session() as session:
            user = await self._user_dao.get_user_id(user_id, session)
        if not user:
            raise ObjectNotFound(f'Can not find user with id: {user_id}')
        return user.balance

    async def process_money_transfer(
            self,
            money_transfer_request: MoneyTransferRequest,
            sender_id: UserId
    ) -> Balance:
        current_sender_balance = 0
        async with self._session() as session:
            transfer_participants = list(await self._user_dao.get_multiple_users_by_ids(
                [sender_id, money_transfer_request.recipient_id],
                session
            ))
            if len(transfer_participants) < 2:
                raise ObjectNotFound('Either sender or recipient do not exists')
            for transfer_participant in transfer_participants:
                if transfer_participant.id == sender_id:
                    current_sender_balance = transfer_participant.balance
            if current_sender_balance < money_transfer_request.amount:
                raise Conflict('Not enough money to process transfer')
            await self._user_dao.process_money_transfer(
                amount_of_money_to_transfer=money_transfer_request.amount,
                sender_id=sender_id,
                recipient_id=money_transfer_request.recipient_id,
                session=session,
                current_sender_balance=current_sender_balance
            )
        return current_sender_balance - money_transfer_request.amount
