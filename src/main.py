from datetime import timedelta, datetime

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Optional

from src.core.models.database import engine
from src.definitions import tags_metadata, config, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from src.core.models import models, crud
from src.v1.dependencies import get_db
from src.v1.endpoints import availability, game, interest, user

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(
    title="Game Lobby API",
    description="An API to support a mobile or web app where users can share "
                "their availability for playing videogames and board games.",
    version="1.0.0",
    tags_metadata=tags_metadata
)
app.include_router(user.router)
app.include_router(availability.router)
app.include_router(interest.router)
app.include_router(game.router)


def verify_password(plain_password: str, hashed_password: str):
    """
    Verifies that the password entered matches the hashed password stored in the
    db.

    :param plain_password: plain-text password
    :param hashed_password: known password hash
    :return: True if password is correct, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str,
                      password: str,
                      db: Session = Depends(get_db)):
    """
    Authenticates a user by checking if their account exists and if their
    password is correct.

    :param username: name associated with account
    :param password: password associated with account
    :param db: database dependency
    :return: False if credentials are incorrect, otherwise returns the info for
    the authenticated user's account
    """
    auth_user = crud.get_user_by_username(db, username)
    if not auth_user or not verify_password(password, auth_user.hashed_password):
        return False

    return auth_user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Takes user data and an expiry delta and returns an access token.

    :param data: user data
    :param expires_delta: token TTL with a default of 15 minutes
    :return: the access token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config['SECRET_KEY'], algorithm=ALGORITHM)

    return encoded_jwt


###############################################################################
# Main functions
###############################################################################
@app.get("/", tags=['root'])
async def get_root(db: Session = Depends(get_db)):
    """
    A list where each object contains a user's name, time available, and the
    game they are interested in playing.

    :param db: database dependency
    :return: list of name/time/game aggregate
    """
    return crud.get_root(db)


@app.post("/token")
async def login_for_access_token(db: Session = Depends(get_db),
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Logs a user in using OAuth2. A user account must be created before that
    user can log in.

    :param db: database dependency
    :param form_data: OAuth2 form data, i.e. username and un-hashed password
    :return: JSON response of access token
    """
    auth_user = authenticate_user(form_data.username, form_data.password, db)

    if not auth_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": auth_user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
