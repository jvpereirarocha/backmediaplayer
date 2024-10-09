from sqlalchemy.orm import registry, Mapped, mapped_column, sessionmaker, scoped_session
from sqlalchemy import Index, create_engine
from os import getenv


mapped_registry = registry()


@mapped_registry.mapped_as_dataclass
class Media:
    __tablename__ = "media"

    media_id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    title: Mapped[str]
    url: Mapped[str] = mapped_column(unique=True)

    __table_args__ = (
        Index('title_url_idx', 'title', 'url'),
        Index('title_idx', 'title'),
        Index('url_idx', 'url'),
    )

engine = None
try:
    engine = create_engine(
        url=getenv("DATABASE_URI")
    )
except Exception:
    raise ValueError("Database URI incorrect")


Session = scoped_session(sessionmaker(bind=engine))


def close_db_session():
    Session.remove()