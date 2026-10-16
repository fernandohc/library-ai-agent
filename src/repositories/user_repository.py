from typing import Optional

from pymongo.database import Database

from src.models.user import User


class UserRepository:
    def __init__(self, database: Database):
        self.collection = database["users"]

    def create(self, user: User) -> User:
        document = user.model_dump(by_alias=True)

        self.collection.insert_one(document)

        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        document = self.collection.find_one({"_id": user_id})

        if not document:
            return None

        return User.model_validate(document)

    def find_all(self) -> list[User]:
        documents = self.collection.find()

        return [User.model_validate(document) for document in documents]

    def delete(self, user_id: str) -> bool:
        result = self.collection.delete_one({"_id": user_id})

        return result.deleted_count > 0

    def get_loan_history(self, user_id: str):
        document = self.collection.find_one({"_id": user_id}, {"loan_history": 1})

        if not document:
            return []

        return document.get("loan_history", [])

    def get_reserved_books(self, user_id: str):
        document = self.collection.find_one({"_id": user_id}, {"reserved_books": 1})

        if not document:
            return []

        return document.get("reserved_books", [])
