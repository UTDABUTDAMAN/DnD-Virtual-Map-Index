from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from project import db

class Location(db.Model):
    __tablename__ = 'location'
    
    # SQLAlchemy 2.0 Typed Mappings
    id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000))
    notes: Mapped[Optional[str]] = mapped_column(String(1000))

    def __repr__(self) -> str:
        return f"<Location {self.name}>"