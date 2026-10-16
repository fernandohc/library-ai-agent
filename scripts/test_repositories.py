from src.database.mongodb import MongoDB
from src.repositories.author_repository import AuthorRepository
from src.repositories.book_copy_repository import BookCopyRepository
from src.repositories.book_repository import BookRepository
from src.repositories.review_repository import ReviewRepository
from src.repositories.user_repository import UserRepository


def main():

    mongo = MongoDB()
    db = mongo.get_database()

    book_repository = BookRepository(db)
    author_repository = AuthorRepository(db)
    copy_repository = BookCopyRepository(db)
    review_repository = ReviewRepository(db)
    user_repository = UserRepository(db)

    print("\n=== DATABASE ===")

    print("Books:", len(book_repository.find_all()))

    print("Authors:", len(author_repository.find_all()))

    print("Users:", len(user_repository.find_all()))

    print("\n=== BOOK SEARCH ===")

    books = book_repository.find_by_genre("Sci-Fi")

    print("Sci-Fi books:", len(books))

    for book in books[:5]:
        print(f"- {book.title} | rating={book.rating.average}")

    print("\n=== HIGH RATED BOOKS ===")

    books = book_repository.find_by_min_rating(4.5)

    print("Books >= 4.5:", len(books))

    print("\n=== BOOK AVAILABILITY ===")

    if books:
        book = books[0]

        available = copy_repository.count_available(book.id)

        print(f"{book.title}: {available} available copies")

    print("\n=== REVIEWS ===")

    if books:
        reviews = review_repository.find_by_book_id(books[0].id)

        print(f"Reviews: {len(reviews)}")

    print("\n=== USER HISTORY ===")

    user = user_repository.find_by_id("user-001")

    if user:
        print(f"{user.name}: {len(user.loan_history)} loans")

        for loan in user.loan_history[:5]:
            print(f"- {loan.book_id} | rating={loan.rating}")

    mongo.close()


if __name__ == "__main__":
    main()
