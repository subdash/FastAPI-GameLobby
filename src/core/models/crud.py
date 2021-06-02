from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.core.models import models
from src.core.schemas import schema


###############################################################################
# Root functions
###############################################################################
def get_root(db: Session):
    """
    Join user, availability and game tables
    """
    return db.query() \
        .with_entities(models.User.username, models.Availability.time_avail,
                       models.Game.name) \
        .filter(models.Availability.user_id == models.User.id) \
        .filter(models.Interest.user_id == models.User.id) \
        .filter(models.Game.id == models.Interest.game_id) \
        .all()


###############################################################################
# User functions
###############################################################################
def get_user(db: Session, user_id: int):
    predicate = models.User.id == user_id
    return db.query(models.User).filter(predicate).first()


def get_user_by_email(db: Session, email: str):
    predicate = models.User.email == email
    return db.query(models.User).filter(predicate).first()


def get_user_by_username(db: Session, username: str):
    predicate = models.User.username == username
    return db.query(models.User).filter(predicate).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User) \
        .offset(skip) \
        .limit(limit) \
        .all()


def create_user(db: Session, user: schema.UserCreate):
    def get_password_hash(password):
        # TODO: Define pwd_context outside of `main` so it is not repeated here
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username,
                          email=user.email,
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


###############################################################################
# Availability functions
###############################################################################
def create_availability(db: Session, availability: schema.AvailabilityCreate):
    db_item = models.Availability(time_avail=availability.time_avail, user_id=availability.user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def read_availability(db: Session, user_id: int, skip: int, limit: int):
    return db.query(models.Availability) \
        .join(models.User) \
        .filter(models.Availability.user_id == user_id) \
        .offset(skip) \
        .limit(limit) \
        .all()


###############################################################################
# Interest functions
###############################################################################
def create_interest(db: Session, user_id: int, game_id: int):
    db_item = models.Interest(user_id=user_id, game_id=game_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def read_interest(db: Session, user_id: int, skip: int, limit: int):
    return db.query(models.Interest) \
        .join(models.User) \
        .filter(models.Interest.user_id == user_id) \
        .offset(skip) \
        .limit(limit) \
        .all()


###############################################################################
# Game functions
###############################################################################
def get_games(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Game).offset(skip).limit(limit).all()
