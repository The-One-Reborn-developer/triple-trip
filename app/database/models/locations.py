from sqlalchemy import Text, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base


class Location(Base):
    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(2))
    name: Mapped[str] = mapped_column(String(200))
    address: Mapped[str] = mapped_column(Text)
    photos: Mapped[list[str]] = mapped_column(JSON)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    def __repr__(self):
        return f'Location(id={self.id}, country={self.country}, name={self.name}, address={self.address}, photos={self.photos}, is_verified={self.is_verified})'