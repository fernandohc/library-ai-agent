from src.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:
    def __init__(self, analytics_repository: AnalyticsRepository):
        self.analytics_repository = analytics_repository

    def get_library_overview(self) -> dict:
        return self.analytics_repository.get_library_overview()

    def get_popular_genres(self, limit: int = 10) -> list[dict]:
        return self.analytics_repository.get_popular_genres(limit)

    def get_top_rated_books(self, limit: int = 10) -> list[dict]:
        return self.analytics_repository.get_top_rated_books(limit)
