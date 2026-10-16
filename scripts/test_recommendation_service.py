from src.database.mongodb import MongoDB
from src.repositories.book_repository import BookRepository
from src.repositories.user_repository import UserRepository
from src.services.recommendation_service import RecommendationService


def main():
    mongodb = MongoDB()

    try:
        database = mongodb.get_database()

        user_repository = UserRepository(database)
        book_repository = BookRepository(database)

        recommendation_service = RecommendationService(
            user_repository=user_repository,
            book_repository=book_repository,
        )

        # Use the exact ID stored in MongoDB.
        user_id = "user-001"

        recommendations = recommendation_service.recommend_books(
            user_id=user_id,
            limit=5,
        )

        print("=== BOOK RECOMMENDATIONS ===")
        print(f"User: {user_id}")
        print(f"Recommendations found: {len(recommendations)}")

        for index, book in enumerate(recommendations, start=1):
            print(f"\n{index}. {book['title']}")
            print(f"   Authors: {', '.join(book['authors'])}")
            print(f"   Genres: {', '.join(book['genres'])}")
            print(f"   Matching genres: {', '.join(book['matching_genres'])}")
            print(f"   Rating: {book['rating']}")
            print(f"   Preference score: {book['preference_score']}")

    finally:
        mongodb.close()


if __name__ == "__main__":
    main()
