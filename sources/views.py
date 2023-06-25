from functools import wraps
from typing import Any, Callable, Coroutine

from fastapi import APIRouter, Depends, status
from loguru import logger

from sources.di_container import create_user_model
from sources.models import UserModel
from sources.schemas.requests import MoneyTransferRequest
from sources.schemas.responces import (BalanceResponse, CreateNewUserResponse,
                                       ErrorResponse, MoneyTransferResponse)
from sources.schemas.test_task_types import (
    DecoratorWithArgumentsForCoroutine, UserId)
from sources.shared.constants import MAIN_VIEW_PREFIX
from sources.shared.exceptions import (EXCEPTION_TO_API_ERROR_MAPPING,
                                       TestTaskError)

user_view = APIRouter(prefix=MAIN_VIEW_PREFIX)


def log_endpoint_activity(
        processed_action: str
) -> DecoratorWithArgumentsForCoroutine:

    def decorator(function: Callable) -> Callable[[tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, Any]]:

        @wraps(function)
        async def wrapper(*args, **kwargs) -> Any:
            logger.debug(f'Processing attempt to {processed_action}')
            try:
                result = await function(*args, **kwargs)
                logger.info(f'Successful attempt to {processed_action}')
                return result
            except TestTaskError as error:
                logger.info(f'Unsuccessful attempt to {processed_action}. Error: {str(error)}')
                http_exception = EXCEPTION_TO_API_ERROR_MAPPING[type(error)]
                http_exception.detail = str(error)
                raise http_exception

        return wrapper

    return decorator


@user_view.post(
    '/create',
    status_code=status.HTTP_200_OK,
    description='Create new user',
    response_model_by_alias=False,
)
@log_endpoint_activity(processed_action='create user')
async def create_new_user(user_model: UserModel = Depends(create_user_model)) -> CreateNewUserResponse:
    new_user_id = await user_model.create_new_user()
    return CreateNewUserResponse(user_id=new_user_id)


@user_view.get(
    '/{user_id}/balance',
    status_code=status.HTTP_200_OK,
    description='Get current balance',
    responses={
        404: {'model': ErrorResponse, 'description': 'User with such id does not exists'},
    },
    response_model_by_alias=False,
)
@log_endpoint_activity(processed_action='get current balance')
async def get_user_balance(user_id: UserId, user_model: UserModel = Depends(create_user_model)) -> BalanceResponse:
    current_balance = await user_model.get_user_balance(user_id)
    return BalanceResponse(balance=current_balance)


@user_view.post(
    '/{user_id}/balance/transfer',
    status_code=status.HTTP_200_OK,
    description='Transfer money from one user to another',
    responses={
        404: {'model': ErrorResponse, 'description': 'Either sender or recipient were not found'},
        409: {'model': ErrorResponse, 'description': 'Not enough money to process transfer'}
    },
    response_model_by_alias=False,
)
@log_endpoint_activity(processed_action='transfer money')
async def process_money_transfer(
        user_id: UserId,
        money_transfer_request: MoneyTransferRequest,
        user_model: UserModel = Depends(create_user_model)
) -> MoneyTransferResponse:
    new_balance = await user_model.process_money_transfer(money_transfer_request, user_id)
    return MoneyTransferResponse(balance=new_balance)
