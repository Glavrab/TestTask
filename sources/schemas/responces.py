from pydantic import BaseModel

from sources.schemas.test_task_types import Balance, UserId


class CreateNewUserResponse(BaseModel):
    user_id: UserId


class BalanceResponse(BaseModel):
    balance: Balance


class MoneyTransferResponse(BalanceResponse):
    pass


class ErrorResponse(BaseModel):
    detail: str
