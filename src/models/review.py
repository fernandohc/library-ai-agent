from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class Review(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., alias="_id")
    user_id: str
    book_id: str

    rating: int = Field(..., ge=1, le=5)

    review: str | None = None
    created_at: date
