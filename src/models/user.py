from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ReservedBook(BaseModel):
    book_id: str = Field(..., description="Book identifier")
    reservation_date: date = Field(
        ..., description="Date when the reservation was created"
    )


class LoanHistory(BaseModel):
    book_id: str = Field(..., description="Book identifier")
    loan_date: date = Field(..., description="Date when the book was borrowed")
    return_date: date | None = Field(
        default=None, description="Date when the book was returned"
    )
    rating: int | None = Field(
        default=None, ge=1, le=5, description="User rating for the book"
    )
    review: str | None = Field(default=None, description="User review")
    delayed: bool = Field(
        default=False, description="Whether the book was returned after the due date"
    )


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., alias="_id")
    name: str
    birth_date: date
    registration_date: date

    reserved_books: list[ReservedBook] = Field(default_factory=list)
    loan_history: list[LoanHistory] = Field(default_factory=list)
