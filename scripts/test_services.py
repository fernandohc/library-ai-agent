from src.database.mongodb import MongoDB
from src.repositories.book_repository import BookRepository
from src.services.book_service import BookService


def main():
    mongodb = MongoDB()
    database = mongodb.get_database()

    book_repository = BookRepository(database)
    book_service = BookService(book_repository)

    print("=== SEARCH BY TITLE ===")

    books = book_service.search_books("Silent")

    for book in books[:5]:
        print(f"- {book.title}")

    print("\n=== SEARCH BY GENRE ===")

    books = book_service.search_by_genre("Sci-Fi")

    print(f"Sci-Fi books: {len(books)}")

    for book in books[:5]:
        print(f"- {book.title}")

    print("\n=== SEARCH BY RATING ===")

    books = book_service.search_by_min_rating(4.5)

    print(f"Books rated >= 4.5: {len(books)}")

    for book in books[:5]:
        print(f"- {book.title} (rating={book.rating.average})")

    mongodb.close()


if __name__ == "__main__":
    main()
