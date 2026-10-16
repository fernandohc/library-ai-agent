from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class BookCopyStatus(str, Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"


class BookCopy(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., alias="_id")
    book_id: str
    status: BookCopyStatus = BookCopyStatus.AVAILABLE
    acquisition_date: date | None = None
    location: str | None = None
