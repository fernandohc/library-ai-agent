from src.models.user import User
from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: str) -> User | None:
        return self.user_repository.find_by_id(user_id)

    def get_loan_history(self, user_id: str):
        return self.user_repository.get_loan_history(user_id)

    def get_reserved_books(self, user_id: str):
        return self.user_repository.get_reserved_books(user_id)
