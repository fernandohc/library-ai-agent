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


@tool(return_direct=True)
def search_available_books_by_genre(genre: str) -> str:
    """
    Find books of a specific genre that have available copies.
    Returns a formatted list of books and the number of available copies.
    Use this tool when the user wants books of a genre
    that can currently be borrowed.
    """

    books = get_container().book_service.search_available_by_genre(genre)

    if not books:
        return f"No available books found for the genre '{genre}'."

    lines = [f"Found {len(books)} available books in the genre '{genre}':"]

    for index, book in enumerate(books, start=1):
        authors = book.get("authors", [])
        author_names = [
            author.get("name", "Unknown") if isinstance(author, dict) else str(author)
            for author in authors
        ]

        genres = book.get("genres", [])
        rating = book.get("rating", {})
        if isinstance(rating, dict):
            rating = rating.get("average")

        lines.append("")
        lines.append(f"{index}. {book.get('title', 'Untitled')}")

        if author_names:
            lines.append(f"   Authors: {', '.join(author_names)}")

        if genres:
            lines.append(f"   Genres: {', '.join(genres)}")

        if rating is not None:
            lines.append(f"   Rating: {rating}")

        lines.append(f"   Available copies: {book.get('available_copies', 0)}")

    return "\n".join(lines)
