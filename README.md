## Purpose
My wife had an idea for an app, and I wanted to take a shot at writing the backend code for it, so I translated her idea into some requirements and built this. The basic idea is:
- A user can create an account
- A user can post their availability
- A user can post which games they are interested in playing
- An authenticated user can view the availability and interests of other users


## Improvements
- Frontend web or mobile interface
- WebSockets integration for real time updates
- Use of [Alembic](https://alembic.sqlalchemy.org/en/latest/) or another migration tool for DB changes
- A "friend's list" of sorts so that users can limit the results they see to people that they know


## Docs
Docs can be viewed when the server is running at http://localhost:8000/docs and http://localhost:8000/redoc


## Testing
We want to start the API server so that the tables are created, create a user, and then create test data that depends on that user, so following these steps in order is important. The scripts are in the `src/scripts` directory. Before starting, have MySQL/MariaDB daemon running with credentials saved in `src/.env`, and a `SECRET_KEY` saved in that file for signing JWTs.
1. Start the API server with `uvicorn src.main:app --reload` from the project root
2. Execute `create_test_user.sh` to create a test user
3. Execute the `seed_db.sql` script to create other test data
4. Run `pytest` from the project root
5. If a step is missed: kill API server, execute `reset_db.sql` script, and then start from step #1


## About
[FastAPI](https://fastapi.tiangolo.com/) is the framework used to build this project. The project is wired to use [MariaDB](https://mariadb.org/), but with a few tweaks another database could be used instead. [SQLAlchemy](https://www.sqlalchemy.org/) was used as an ORM to keep the code that interacts with the DB clean and correct.
