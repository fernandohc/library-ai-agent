import re
from typing import Optional

from pymongo.database import Database

from src.models.book import Book


class BookRepository:
    def __init__(self, database: Database):
        self.collection = database["books"]

    def create(self, book: Book) -> Book:
        document = book.model_dump(by_alias=True)

        self.collection.insert_one(document)

        return book

    def find_by_id(self, book_id: str) -> Optional[Book]:
        document = self.collection.find_one({"_id": book_id})

        if not document:
            return None

        return Book.model_validate(document)

    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        document = self.collection.find_one({"isbn": isbn})

        if not document:
            return None

        return Book.model_validate(document)

    def find_by_title(self, title: str) -> list[Book]:
        documents = self.collection.find({"title": {"$regex": title, "$options": "i"}})

        return [Book.model_validate(document) for document in documents]

    def find_by_author(self, author_id: str) -> list[Book]:
        documents = self.collection.find({"authors.author_id": author_id})

        return [Book.model_validate(document) for document in documents]

    def find_by_genre(self, genre: str) -> list[Book]:
        documents = self.collection.find(
            {"genres": {"$regex": f"^{genre}$", "$options": "i"}}
        )

        return [Book.model_validate(document) for document in documents]

    def find_by_min_rating(self, rating: float) -> list[Book]:

        documents = self.collection.find({"rating.average": {"$gte": rating}})

        return [Book.model_validate(document) for document in documents]

    def find_by_max_pages(self, pages: int) -> list[Book]:

        documents = self.collection.find({"metadata.pages": {"$lte": pages}})

        return [Book.model_validate(document) for document in documents]

    def find_all(self) -> list[Book]:
        documents = self.collection.find()

        return [Book.model_validate(document) for document in documents]

    def delete(self, book_id: str) -> bool:
        result = self.collection.delete_one({"_id": book_id})

        return result.deleted_count > 0

    def find_available_by_genre(self, genre: str) -> list[dict]:
        pipeline = [
            {
                "$match": {
                    "genres": {
                        "$regex": f"^{re.escape(genre)}$",
                        "$options": "i",
                    }
                }
            },
            {
                "$lookup": {
                    "from": "book_copies",
                    "localField": "_id",
                    "foreignField": "book_id",
                    "pipeline": [
                        {"$match": {"status": "available"}},
                        {"$count": "count"},
                    ],
                    "as": "availability",
                }
            },
            {
                "$addFields": {
                    "available_copies": {
                        "$ifNull": [
                            {
                                "$arrayElemAt": [
                                    "$availability.count",
                                    0,
                                ]
                            },
                            0,
                        ]
                    }
                }
            },
            {"$match": {"available_copies": {"$gt": 0}}},
            {
                "$project": {
                    "_id": 0,
                    "title": 1,
                    "authors.name": 1,
                    "genres": 1,
                    "rating.average": 1,
                    "available_copies": 1,
                }
            },
        ]

        return list(self.collection.aggregate(pipeline))
