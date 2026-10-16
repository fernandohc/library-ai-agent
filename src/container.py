from src.database.mongodb import MongoDB
from src.repositories.analytics_repository import AnalyticsRepository
from src.repositories.book_copy_repository import BookCopyRepository
from src.repositories.book_repository import BookRepository
from src.repositories.review_repository import ReviewRepository
from src.repositories.user_repository import UserRepository
from src.services.analytics_service import AnalyticsService
from src.services.availability_service import AvailabilityService
from src.services.book_service import BookService
from src.services.recommendation_service import RecommendationService
from src.services.user_service import UserService


class ApplicationContainer:
    def __init__(self):
        self.mongodb = MongoDB()
        database = self.mongodb.get_database()

        # Repositories
        self.book_repository = BookRepository(database)
        self.book_copy_repository = BookCopyRepository(database)
        self.user_repository = UserRepository(database)
        self.review_repository = ReviewRepository(database)
        self.analytics_repository = AnalyticsRepository(database)

        # Services
        self.book_service = BookService(self.book_repository)

        self.availability_service = AvailabilityService(self.book_copy_repository)

        self.user_service = UserService(self.user_repository)

        self.recommendation_service = RecommendationService(
            user_repository=self.user_repository,
            book_repository=self.book_repository,
        )

        self.analytics_service = AnalyticsService(self.analytics_repository)

    def close(self):
        self.mongodb.close()


_container = None


def get_container() -> ApplicationContainer:
    global _container

    if _container is None:
        _container = ApplicationContainer()

    return _container


def close_container():
    global _container

    if _container is not None:
        _container.close()
        _container = None
