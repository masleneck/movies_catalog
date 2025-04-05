from datetime import date
from sqlalchemy import BigInteger, Text, Date
from sqlalchemy.dialects.postgresql import CITEXT, SMALLINT
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Movie(Base):
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        )
    title: Mapped[str] = mapped_column(
        CITEXT(120),
        index=True,
    )
    description: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default=""
    )
    release_date: Mapped[date | None] = mapped_column(
        Date,
    )
    duration: Mapped[int | None] = mapped_column(
        SMALLINT,
    )
    # TODO: age rating relation

    def __str__(self) -> str:
        return self.title
    
    def __repr__(self) -> str:
        return f"Movie(id={self.id}, title={self.title!r})"