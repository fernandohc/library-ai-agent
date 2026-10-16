from src.models.book import Book
from src.repositories.book_repository import BookRepository


class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def search_books(self, title: str) -> list[Book]:
        return self.book_repository.find_by_title(title)

    def get_book(self, book_id: str) -> Book | None:
        return self.book_repository.find_by_id(book_id)

    def search_by_author(self, author_id: str) -> list[Book]:
        return self.book_repository.find_by_author(author_id)

    def search_by_genre(self, genre: str) -> list[Book]:
        return self.book_repository.find_by_genre(genre)

    def search_by_min_rating(self, rating: float) -> list[Book]:
        return self.book_repository.find_by_min_rating(rating)

    def search_by_max_pages(self, pages: int) -> list[Book]:
        return self.book_repository.find_by_max_pages(pages)

    def search_available_by_genre(self, genre: str) -> list[dict]:
        return self.book_repository.find_available_by_genre(genre)
