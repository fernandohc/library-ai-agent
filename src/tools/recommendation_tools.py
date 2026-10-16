from langchain_core.tools import tool

from src.container import get_container


@tool
def recommend_books_for_user(
    user_id: str,
    limit: int = 5,
    min_rating: int = 4,
) -> list[dict]:
    """
    Recommend books based on a user's loan history and ratings.

    Use this tool when the user asks for personalized book
    recommendations. The user ID must be provided explicitly.

    Returns recommended books, their ratings, matching genres,
    and preference scores.
    """
    return get_container().recommendation_service.recommend_books(
        user_id=user_id,
        limit=limit,
        min_rating=min_rating,
    )
