from typing import Optional

from pymongo.database import Database

from src.models.review import Review


class ReviewRepository:
    def __init__(self, database: Database):
        self.collection = database["reviews"]

    def create(self, review: Review) -> Review:
        document = review.model_dump(by_alias=True)

        self.collection.insert_one(document)

        return review

    def find_by_id(self, review_id: str) -> Optional[Review]:

        document = self.collection.find_one({"_id": review_id})

        if not document:
            return None

        return Review.model_validate(document)

    def find_by_book_id(self, book_id: str) -> list[Review]:

        documents = self.collection.find({"book_id": book_id})

        return [Review.model_validate(document) for document in documents]

    def find_by_user_id(self, user_id: str) -> list[Review]:

        documents = self.collection.find({"user_id": user_id})

        return [Review.model_validate(document) for document in documents]

    def find_by_rating(self, minimum_rating: int) -> list[Review]:

        documents = self.collection.find({"rating": {"$gte": minimum_rating}})

        return [Review.model_validate(document) for document in documents]
