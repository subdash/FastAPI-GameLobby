from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

from src.core.models import crud
from src.core.models.models import User
from src.core.schemas import schema
from src.v1.dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@router.post("/", response_model=schema.User, tags=['user'])
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint for creating an account,

    :param user: user data, including username, email and password
    :param db: database dependency
    :return: JSON response of username, email, availability, interest, and
    whether the account is disabled
    """
    existing_user = crud.get_user_by_username(db, username=user.username)
    existing_email = crud.get_user_by_email(db, email=user.email)

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username already registered")

    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")

    crud.create_user(db=db, user=user)

    # This should redirect the user to their account (/users/{user_id}/), but
    # that requires wiring in authentication to this call.
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    # return RedirectResponse(url="/users/user_id/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/", response_model=List[schema.User])
async def read_users(skip: int = 0,
                     limit: int = 100,
                     current_user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    """
    Endpoint for getting a list of users accounts.

    :param skip: how many users to skip
    :param limit: how many total users
    :param current_user: the currently logged in user
    :param db: database dependency
    :return: JSON response of a set of user accounts
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}/", response_model=schema.User)
async def read_user(user_id: int,
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """
    Endpoint for retrieving a single user account.

    :param user_id: the id of the user in the database
    :param current_user: the currently logged in user
    :param db: database dependency
    :return: JSON response of user information
    """
    db_user = crud.get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return current_user
