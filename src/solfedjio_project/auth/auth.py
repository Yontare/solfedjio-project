import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend

from auth.manager import get_user_manager
from db.db_config import User

SECRET = ""
cookie_transport = CookieTransport(cookie_max_age=36000000)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=36000000)


auth_backend = AuthenticationBackend(name="jwt", transport=cookie_transport, get_strategy=get_jwt_strategy, )
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend], )
