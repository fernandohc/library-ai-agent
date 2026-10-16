from typing import Optional

from pymongo.database import Database

from src.models.author import Author


class AuthorRepository:
    def __init__(self, database: Database):
        self.collection = database["authors"]

    def create(self, author: Author) -> Author:
        document = author.model_dump(by_alias=True)

        self.collection.insert_one(document)

        return author

    def find_by_id(self, author_id: str) -> Optional[Author]:

        document = self.collection.find_one({"_id": author_id})

        if not document:
            return None

        return Author.model_validate(document)

    def find_by_name(self, name: str) -> list[Author]:

        documents = self.collection.find({"name": {"$regex": name, "$options": "i"}})

        return [Author.model_validate(document) for document in documents]

    def find_all(self) -> list[Author]:
        documents = self.collection.find()

        return [Author.model_validate(document) for document in documents]
