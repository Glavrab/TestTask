from sources.db import generate_async_session
from sources.db.dao import User
from sources.models import UserModel


def create_user_model() -> UserModel:
    return UserModel(user_dao=User, session=generate_async_session())
