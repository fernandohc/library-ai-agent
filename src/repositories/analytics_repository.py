class AnalyticsRepository:
    def __init__(self, database):
        self.database = database
        self.books = database["books"]
        self.authors = database["authors"]
        self.users = database["users"]
        self.book_copies = database["book_copies"]

    def get_library_overview(self) -> dict:
        copies_by_status = list(
            self.book_copies.aggregate(
                [
                    {
                        "$group": {
                            "_id": "$status",
                            "count": {"$sum": 1},
                        }
                    },
                    {"$sort": {"_id": 1}},
                ]
            )
        )

        return {
            "total_books": self.books.count_documents({}),
            "total_authors": self.authors.count_documents({}),
            "total_users": self.users.count_documents({}),
            "total_copies": self.book_copies.count_documents({}),
            "copies_by_status": {
                item["_id"]: item["count"] for item in copies_by_status
            },
        }

    def get_popular_genres(self, limit: int = 10) -> list[dict]:
        return list(
            self.books.aggregate(
                [
                    {"$unwind": "$genres"},
                    {
                        "$group": {
                            "_id": "$genres",
                            "book_count": {"$sum": 1},
                        }
                    },
                    {"$sort": {"book_count": -1, "_id": 1}},
                    {"$limit": limit},
                    {
                        "$project": {
                            "_id": 0,
                            "genre": "$_id",
                            "book_count": 1,
                        }
                    },
                ]
            )
        )

    def get_top_rated_books(self, limit: int = 10) -> list[dict]:
        return list(
            self.books.aggregate(
                [
                    {"$match": {"rating.average": {"$gt": 0}}},
                    {
                        "$sort": {
                            "rating.average": -1,
                            "rating.count": -1,
                        }
                    },
                    {"$limit": limit},
                    {
                        "$project": {
                            "_id": 1,
                            "title": 1,
                            "authors": 1,
                            "genres": 1,
                            "rating": 1,
                        }
                    },
                ]
            )
        )
