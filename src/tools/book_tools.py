from langchain_core.tools import tool

from src.container import get_container


@tool
def search_books(title: str) -> list[dict]:
    """
    Search books by title.

    Use this tool when the user is looking for a book
    based on its title or part of its title.
    """

    books = get_container().book_service.search_books(title)

    return [
        {
            "id": book.id,
            "title": book.title,
            "authors": [author.name for author in book.authors],
            "genres": book.genres,
            "rating": book.rating.average,
        }
        for book in books
    ]


@tool
def search_available_books_by_genre(genre: str) -> list[dict]:
    """
    Find books of a specific genre that have available copies.
    Returns book details and the number of available copies.
    Use this tool when the user wants books of a genre
    that can currently be borrowed.
    """

    return get_container().book_service.search_available_by_genre(genre)


@tool
def get_book(book_id: str) -> dict | None:
    """
    Get detailed information about a book using its ID.
    """

    book = get_container().book_service.get_book(book_id)

    if not book:
        return None

    return {
        "id": book.id,
        "title": book.title,
        "isbn": book.isbn,
        "published_year": book.published_year,
        "authors": [
            {
                "id": author.author_id,
                "name": author.name,
            }
            for author in book.authors
        ],
        "genres": book.genres,
        "pages": book.metadata.pages,
        "language": book.metadata.language,
        "publisher": book.metadata.publisher,
        "rating": book.rating.average,
        "rating_count": book.rating.count,
    }


@tool
def search_books_by_genre(genre: str) -> list[dict]:
    """
    Search books belonging to a specific genre.
    """

    books = get_container().book_service.search_by_genre(genre)

    return [
        {
            "id": book.id,
            "title": book.title,
            "authors": [author.name for author in book.authors],
            "genres": book.genres,
            "rating": book.rating.average,
        }
        for book in books
    ]


@tool
def search_books_by_author(author_id: str) -> list[dict]:
    """
    Search books written by a specific author.
    """

    books = get_container().book_service.search_by_author(author_id)

    return [
        {
            "id": book.id,
            "title": book.title,
            "authors": [author.name for author in book.authors],
            "genres": book.genres,
            "rating": book.rating.average,
        }
        for book in books
    ]


@tool
def check_availability(book_id: str) -> dict:
    """
    Check how many copies of a book are currently available.
    """

    available_copies = get_container().availability_service.check_availability(book_id)

    return {
        "book_id": book_id,
        "available_copies": available_copies,
        "available": available_copies > 0,
    }
