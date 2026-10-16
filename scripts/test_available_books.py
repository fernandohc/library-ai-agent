from src.database.mongodb import MongoDB
from src.repositories.book_repository import BookRepository
from src.services.book_service import BookService


def main():
    mongodb = MongoDB()

    try:
        database = mongodb.get_database()
        repository = BookRepository(database)
        service = BookService(repository)

        books = service.search_available_by_genre("Horror")

        print("=== AVAILABLE HORROR BOOKS ===")
        print(f"Books found: {len(books)}")

        for book in books:
            authors = [author["name"] for author in book.get("authors", [])]

            print(
                f"- {book['title']} | "
                f"Authors: {', '.join(authors)} | "
                f"Available copies: {book['available_copies']}"
            )

    finally:
        mongodb.close()


if __name__ == "__main__":
    main()
