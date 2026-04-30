from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.infrastructure.settings.settings import settings

engine = create_engine(
    settings.database_url,
    echo=settings.is_development,
    pool_pre_ping=True,
)


session_factory: sessionmaker[Session] = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


class Base(DeclarativeBase): ...


def get_db_session() -> Generator[Session, None, None]:
    with session_factory() as session:
        yield session
