from src.repositories.book_copy_repository import BookCopyRepository


class AvailabilityService:
    def __init__(self, book_copy_repository: BookCopyRepository):
        self.book_copy_repository = book_copy_repository

    def check_availability(self, book_id: str) -> int:
        return self.book_copy_repository.count_available(book_id)
