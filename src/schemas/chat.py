from typing import Literal

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
        description="Question submitted to the library assistant.",
    )


class AskResponse(BaseModel):
    agent: Literal[
        "book_search",
        "recommendation",
        "analytics",
    ]
    answer: str
