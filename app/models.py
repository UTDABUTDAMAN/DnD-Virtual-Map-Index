from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app import db

class Location(db.Model):
    __tablename__ = 'location'
    
    # SQLAlchemy 2.0 Typed Mappings
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    notes: Mapped[Optional[str]] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"<Location {self.name}>"