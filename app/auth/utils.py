from fastapi.security import OAuth2PasswordBearer

from app.auth.db import fake_users_db
from app.models.user import UserInDB


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)