from collections import Counter

from src.repositories.book_repository import BookRepository
from src.repositories.user_repository import UserRepository


class RecommendationService:
    def __init__(
        self,
        user_repository: UserRepository,
        book_repository: BookRepository,
    ):
        self.user_repository = user_repository
        self.book_repository = book_repository

    def recommend_books(
        self,
        user_id: str,
        limit: int = 5,
        min_rating: int = 4,
    ) -> list[dict]:

        # 1. Retrieve the user and their loan history.
        user = self.user_repository.find_by_id(user_id)

        if user is None:
            raise ValueError(f"User not found: {user_id}")

        history = user.loan_history

        if not history:
            return []

        # 2. Identify all books already borrowed by the user.
        borrowed_book_ids = {loan.book_id for loan in history}

        # 3. Identify genres from positively rated books.
        preferred_genres = Counter()

        all_books = self.book_repository.find_all()
        books_by_id = {book.id: book for book in all_books}

        for loan in history:
            if loan.rating is None or loan.rating < min_rating:
                continue

            book = books_by_id.get(loan.book_id)

            if book is None:
                continue

            for genre in set(book.genres):
                preferred_genres[genre] += 1

        if not preferred_genres:
            return []

        # 4. Find books in preferred genres that the user
        # has not borrowed before.
        recommendations = []

        for book in all_books:
            if book.id in borrowed_book_ids:
                continue

            matching_genres = [
                genre for genre in book.genres if genre in preferred_genres
            ]

            if not matching_genres:
                continue

            # 5. Calculate a simple recommendation score.
            preference_score = sum(preferred_genres[genre] for genre in matching_genres)

            rating = book.rating.average or 0.0

            recommendations.append(
                {
                    "book_id": book.id,
                    "title": book.title,
                    "authors": [author.name for author in book.authors],
                    "genres": book.genres,
                    "rating": book.rating.average,
                    "rating_count": book.rating.count,
                    "matching_genres": matching_genres,
                    "preference_score": preference_score,
                }
            )

        # 6. Prefer stronger genre matches, then higher ratings.
        recommendations.sort(
            key=lambda item: (
                item["preference_score"],
                item["rating"] or 0.0,
                item["rating_count"],
            ),
            reverse=True,
        )

        return recommendations[:limit]
