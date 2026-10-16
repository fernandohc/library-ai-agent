from typing import Optional

from pymongo.database import Database

from src.models.book_copy import BookCopy, BookCopyStatus


class BookCopyRepository:
    def __init__(self, database: Database):
        self.collection = database["book_copies"]

    def create(self, book_copy: BookCopy) -> BookCopy:
        document = book_copy.model_dump(by_alias=True)

        self.collection.insert_one(document)

        return book_copy

    def find_by_id(self, copy_id: str) -> Optional[BookCopy]:

        document = self.collection.find_one({"_id": copy_id})

        if not document:
            return None

        return BookCopy.model_validate(document)

    def find_by_book_id(self, book_id: str) -> list[BookCopy]:

        documents = self.collection.find({"book_id": book_id})

        return [BookCopy.model_validate(document) for document in documents]

    def find_available_by_book_id(self, book_id: str) -> list[BookCopy]:

        documents = self.collection.find(
            {"book_id": book_id, "status": BookCopyStatus.AVAILABLE.value}
        )

        return [BookCopy.model_validate(document) for document in documents]

    def count_available(self, book_id: str) -> int:

        return self.collection.count_documents(
            {"book_id": book_id, "status": BookCopyStatus.AVAILABLE.value}
        )

    def update_status(self, copy_id: str, status: BookCopyStatus) -> bool:

        result = self.collection.update_one(
            {"_id": copy_id}, {"$set": {"status": status.value}}
        )

        return result.modified_count > 0
