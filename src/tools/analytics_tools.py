from langchain_core.tools import tool

from src.container import get_container


@tool
def get_library_overview() -> dict:
    """Get general library statistics, including total books,
    authors, users, copies, and copy counts grouped by status."""
    return get_container().analytics_service.get_library_overview()


@tool
def get_popular_genres(limit: int = 10) -> list[dict]:
    """Get the genres with the largest number of books in the
    library. Use this for questions about genre distribution
    or the most common genres."""
    return get_container().analytics_service.get_popular_genres(limit)


@tool
def get_top_rated_books(limit: int = 10) -> list[dict]:
    """Get the highest-rated books, ordered by average rating
    and then by number of ratings. Use this for questions about
    the best-rated books in the library."""
    return get_container().analytics_service.get_top_rated_books(limit)
