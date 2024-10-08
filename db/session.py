from sqlalchemy.orm import registry, Mapped, mapped_column
from sqlalchemy import Index


mapped_registry = registry()


@mapped_registry.mapped_as_dataclass
class Media:
    media_id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    title: Mapped[str]
    url: Mapped[str] = mapped_column(unique=True)

    __table_args__ = (
        Index('title_url_idx', 'title', 'url')
    )