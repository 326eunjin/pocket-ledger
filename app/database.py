from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from fastapi import Request


class Base(DeclarativeBase):
    pass


def make_engine(database_url: str):
    return create_engine(database_url, connect_args={"check_same_thread": False})


def get_session(request: Request):
    with Session(request.app.state.engine) as session:
        yield session
