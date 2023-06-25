import random

import pytest
from httpx import AsyncClient

from sources.di_container import create_user_model
from sources.schemas.requests import MoneyTransferRequest
from sources.schemas.responces import (BalanceResponse, CreateNewUserResponse,
                                       MoneyTransferResponse)
from sources.shared.constants import BASE_USER_BALANCE, MAIN_VIEW_PREFIX

BASE_API_URL = f'http://localhost:8080{MAIN_VIEW_PREFIX}'
SUCCESSFUL_STATUS_CODE = 200
TEST_DATA = {}


@pytest.mark.asyncio
async def test_user_creation() -> None:
    async with AsyncClient() as client:
        create_new_user_response = await client.post(f'{BASE_API_URL}/create')
    assert create_new_user_response.status_code == SUCCESSFUL_STATUS_CODE
    new_user_data = CreateNewUserResponse.parse_obj(create_new_user_response.json())
    TEST_DATA['user_id'] = new_user_data.user_id


@pytest.mark.asyncio
async def test_getting_balance() -> None:
    non_existing_user_id = random.randint(100, 501)
    endpoint_url_pattern = '{api_url}/{user_id}/balance'
    async with AsyncClient() as client:
        invalid_response_for_non_existing_user = await client.get(
            endpoint_url_pattern.format(api_url=BASE_API_URL, user_id=non_existing_user_id)
        )
        assert invalid_response_for_non_existing_user.status_code == 404
        user_balance_response = await client.get(
            endpoint_url_pattern.format(api_url=BASE_API_URL, user_id=TEST_DATA['user_id'])
        )
    assert user_balance_response.status_code == SUCCESSFUL_STATUS_CODE
    new_user_balance = BalanceResponse.parse_obj(user_balance_response.json())
    assert new_user_balance.balance == BASE_USER_BALANCE


@pytest.mark.asyncio
async def test_money_transfer() -> None:
    user_model = create_user_model()
    new_user_id = await user_model.create_new_user()
    invalid_amount_of_money_to_transfer = random.randint(BASE_USER_BALANCE + 1, BASE_USER_BALANCE * 2)
    amount_of_money_to_transfer = random.randint(1, BASE_USER_BALANCE - 1)
    endpoint_url_pattern = '{api_url}/{user_id}/balance/transfer'
    async with AsyncClient() as client:
        invalid_money_transfer_response = await client.post(
            endpoint_url_pattern.format(api_url=BASE_API_URL, user_id=TEST_DATA['user_id']),
            json=MoneyTransferRequest(amount=invalid_amount_of_money_to_transfer, recipient_id=new_user_id).dict()
        )
        assert invalid_money_transfer_response.status_code == 409
        money_transfer_response = await client.post(
            endpoint_url_pattern.format(api_url=BASE_API_URL, user_id=TEST_DATA['user_id']),
            json=MoneyTransferRequest(amount=amount_of_money_to_transfer, recipient_id=new_user_id).dict(),
        )
    assert money_transfer_response.status_code == SUCCESSFUL_STATUS_CODE
    updated_balance = MoneyTransferResponse.parse_obj(money_transfer_response.json())
    assert updated_balance.balance == BASE_USER_BALANCE - amount_of_money_to_transfer
    assert await user_model.get_user_balance(new_user_id) == BASE_USER_BALANCE + amount_of_money_to_transfer
