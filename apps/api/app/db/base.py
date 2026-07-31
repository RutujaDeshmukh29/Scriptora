"""
Declarative base for all ORM models. Every model in app/models/ must inherit
from this `Base` so Alembic's autogenerate can see it via Base.metadata.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
