from pydantic import BaseModel, ConfigDict, Field


class BookAuthor(BaseModel):
    author_id: str = Field(..., description="Author identifier")
    name: str


class BookMetadata(BaseModel):
    pages: int | None = Field(default=None, gt=0, description="Number of pages")
    language: str | None = None
    publisher: str | None = None


class BookRating(BaseModel):
    average: float | None = Field(default=None, ge=1, le=5)
    count: int = Field(default=0, ge=0)


class Book(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., alias="_id")
    title: str
    isbn: str
    published_year: int

    authors: list[BookAuthor] = Field(default_factory=list)
    genres: list[str] = Field(default_factory=list)

    metadata: BookMetadata = Field(default_factory=BookMetadata)

    rating: BookRating = Field(default_factory=BookRating)
