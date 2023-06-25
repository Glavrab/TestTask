from pydantic import BaseModel, Field

from sources.schemas.test_task_types import UserId


class MoneyTransferRequest(BaseModel):
    recipient_id: UserId
    amount: int = Field(..., gt=0)
