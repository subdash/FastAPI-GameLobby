from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from src.core.models import crud
from src.core.models.database import SessionLocal
from src.core.schemas.schema import TokenData
from src.definitions import config, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    """
    Dependency to get db session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Dependency to retrieve the information of the currently authenticated user.

    :param db: database dependency
    :param token: OAuth token dependency
    :return: currently authenticated user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW_Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, config['SECRET_KEY'], algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError as e:
        print(e)
        raise credentials_exception

    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception

    return user
