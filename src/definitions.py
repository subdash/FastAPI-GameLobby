import os

from dotenv import dotenv_values

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
config = {**dotenv_values(f"{ROOT_DIR}/.env")}
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

tags_metadata = [
    {
        "name": "root",
        "description": "Operations for the home page of the app."
    },
    {
        "name": "user",
        "description": "Operations for users of the app."
    },
    {
        "name": "availability",
        "description": "The time a user is available to play."
    },
    {
        "name": "interest",
        "description": "Which games a user is interested in playing."
    },
    {
        "name": "game",
        "description": "Games that users can share their interest in."
    }
]
