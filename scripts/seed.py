import os
import random
from datetime import datetime, timedelta

from dotenv import load_dotenv
from faker import Faker
from pymongo import MongoClient

load_dotenv()

fake = Faker()

random.seed(42)
Faker.seed(42)


MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://library_app:library_app_password@localhost:27017/library_ai?authSource=library_ai",
)

MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "library_ai")


GENRES = [
    "Horror",
    "Thriller",
    "Children's",
    "Teens",
    "Romance",
    "Sci-Fi",
    "History",
    "Technical",
    "Fantasy",
    "Mystery",
    "Biography",
    "Adventure",
    "Drama",
    "Philosophy",
    "Self-Help",
]


BOOK_TEMPLATES = [
    ("The Silent House", ["Horror", "Mystery"]),
    ("The Last Shadow", ["Thriller", "Mystery"]),
    ("Stars Beyond Earth", ["Sci-Fi", "Adventure"]),
    ("Love in December", ["Romance", "Drama"]),
    ("The Forgotten Kingdom", ["Fantasy", "Adventure"]),
    ("World War Chronicles", ["History", "Biography"]),
    ("Python in Practice", ["Technical"]),
    ("Building Distributed Systems", ["Technical"]),
    ("The Young Detective", ["Children's", "Mystery"]),
    ("Secrets of the Academy", ["Teens", "Mystery"]),
    ("The Lost Expedition", ["Adventure", "History"]),
    ("Mind and Meaning", ["Philosophy"]),
    ("Understanding Yourself", ["Self-Help"]),
    ("The Haunted Library", ["Horror", "Fantasy"]),
    ("Beyond the Stars", ["Sci-Fi"]),
]


def random_date(start_year=2018, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)

    days = (end - start).days

    return start + timedelta(days=random.randint(0, days))


def generate_authors(count=40):
    authors = []

    for index in range(count):
        author_id = f"author-{index + 1:03d}"

        authors.append(
            {
                "_id": author_id,
                "name": fake.name(),
                "country": fake.country(),
                "birth_date": random_date(1940, 1995),
            }
        )

    return authors


def generate_books(authors, count=150):
    books = []

    for index in range(count):
        book_id = f"book-{index + 1:04d}"

        title, genres = random.choice(BOOK_TEMPLATES)

        # Make titles unique
        title = f"{title} {index + 1}"

        selected_authors = random.sample(authors, k=random.choice([1, 1, 1, 2]))

        books.append(
            {
                "_id": book_id,
                "title": title,
                "isbn": f"978-{random.randint(1000000000, 9999999999)}",
                "published_year": random.randint(1950, 2025),
                "authors": [
                    {
                        "author_id": author["_id"],
                        "name": author["name"],
                    }
                    for author in selected_authors
                ],
                "genres": genres,
                "metadata": {
                    "pages": random.randint(120, 900),
                    "language": random.choice(
                        [
                            "English",
                            "Portuguese",
                            "Spanish",
                        ]
                    ),
                    "publisher": fake.company(),
                },
                "rating": {
                    "average": None,
                    "count": 0,
                },
            }
        )

    return books


def generate_users(count=50):
    users = []

    for index in range(count):
        user_id = f"user-{index + 1:03d}"

        users.append(
            {
                "_id": user_id,
                "name": fake.name(),
                "birth_date": random_date(1960, 2005),
                "registration_date": random_date(2020, 2026),
                "reserved_books": [],
                "loan_history": [],
            }
        )

    return users


def generate_book_copies(books):
    copies = []

    copy_number = 1

    for book in books:
        number_of_copies = random.randint(1, 4)

        for _ in range(number_of_copies):
            status = random.choices(
                [
                    "available",
                    "borrowed",
                    "reserved",
                    "maintenance",
                ],
                weights=[
                    55,
                    30,
                    10,
                    5,
                ],
            )[0]

            copies.append(
                {
                    "_id": f"copy-{copy_number:05d}",
                    "book_id": book["_id"],
                    "status": status,
                    "acquisition_date": random_date(2018, 2026),
                    "location": random.choice(
                        [
                            "A1",
                            "A2",
                            "B1",
                            "B2",
                            "C1",
                            "C2",
                        ]
                    ),
                }
            )

            copy_number += 1

    return copies


def generate_reviews(books, users, count=350):
    reviews = []

    for index in range(count):
        book = random.choice(books)
        user = random.choice(users)

        rating = random.choices(
            [1, 2, 3, 4, 5],
            weights=[
                3,
                5,
                15,
                35,
                42,
            ],
        )[0]

        reviews.append(
            {
                "_id": f"review-{index + 1:05d}",
                "user_id": user["_id"],
                "book_id": book["_id"],
                "rating": rating,
                "review": fake.paragraph(nb_sentences=random.randint(1, 3)),
                "created_at": random_date(2022, 2026),
            }
        )

    return reviews


def update_book_ratings(books, reviews):
    ratings = {}

    for review in reviews:
        book_id = review["book_id"]

        ratings.setdefault(book_id, [])

        ratings[book_id].append(review["rating"])

    for book in books:
        book_ratings = ratings.get(book["_id"], [])

        if not book_ratings:
            book["rating"] = {
                "average": None,
                "count": 0,
            }

            continue

        book["rating"] = {
            "average": round(sum(book_ratings) / len(book_ratings), 2),
            "count": len(book_ratings),
        }


def generate_loan_history(users, books, reviews, min_loans=5, max_loans=15):
    """
    Generate borrowing history for each user.

    The history is based on existing reviews whenever possible,
    ensuring that ratings and reviews remain consistent.
    """

    reviews_by_user = {}

    for review in reviews:
        reviews_by_user.setdefault(review["user_id"], []).append(review)

    for user in users:
        user_reviews = reviews_by_user.get(user["_id"], [])

        reviewed_book_ids = {review["book_id"] for review in user_reviews}

        available_book_ids = [
            book["_id"] for book in books if book["_id"] not in reviewed_book_ids
        ]

        number_of_loans = random.randint(min_loans, max_loans)

        selected_book_ids = random.sample(
            available_book_ids, min(number_of_loans, len(available_book_ids))
        )

        loan_history = []

        # First, create loans for books that the user reviewed.
        for review in user_reviews:
            loan_date = random_date(2022, 2026)

            return_date = loan_date + timedelta(days=random.randint(7, 30))

            loan_history.append(
                {
                    "book_id": review["book_id"],
                    "loan_date": loan_date,
                    "return_date": return_date,
                    "rating": review["rating"],
                    "review": review["review"],
                    "delayed": random.random() < 0.15,
                }
            )

        # Then add additional loans without reviews.
        for book_id in selected_book_ids:
            loan_date = random_date(2022, 2026)

            return_date = loan_date + timedelta(days=random.randint(7, 30))

            loan_history.append(
                {
                    "book_id": book_id,
                    "loan_date": loan_date,
                    "return_date": return_date,
                    "rating": None,
                    "review": None,
                    "delayed": random.random() < 0.15,
                }
            )

        user["loan_history"] = loan_history


def create_indexes(db):

    db.books.create_index("isbn", unique=True)

    db.books.create_index("authors.author_id")

    db.books.create_index("genres")

    db.authors.create_index("name")

    db.book_copies.create_index("book_id")

    db.book_copies.create_index(
        [
            ("book_id", 1),
            ("status", 1),
        ]
    )

    db.reviews.create_index("book_id")

    db.reviews.create_index("user_id")


def main():

    print("Connecting to MongoDB...")

    client = MongoClient(MONGODB_URI)

    db = client[MONGODB_DATABASE]

    print("Cleaning collections...")

    collections = [
        "users",
        "books",
        "authors",
        "book_copies",
        "reviews",
    ]

    for collection in collections:
        db[collection].delete_many({})

    print("Generating authors...")

    authors = generate_authors()

    print("Generating books...")

    books = generate_books(authors)

    print("Generating users...")

    users = generate_users()

    print("Generating book copies...")

    book_copies = generate_book_copies(books)

    print("Generating reviews...")

    reviews = generate_reviews(books, users)

    print("Generating loan history...")

    generate_loan_history(users, books, reviews)

    print("Calculating book ratings...")

    update_book_ratings(books, reviews)

    print("Inserting data...")

    db.authors.insert_many(authors)
    db.books.insert_many(books)
    db.users.insert_many(users)
    db.book_copies.insert_many(book_copies)
    db.reviews.insert_many(reviews)

    print("Creating indexes...")

    create_indexes(db)

    print()
    print("Seed completed successfully.")
    print()
    print(f"Authors:      {len(authors)}")
    print(f"Books:        {len(books)}")
    print(f"Users:        {len(users)}")
    print(f"Book copies:  {len(book_copies)}")
    print(f"Reviews:      {len(reviews)}")

    client.close()


if __name__ == "__main__":
    main()
