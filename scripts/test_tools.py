from src.tools.book_tools import (
    check_availability,
    search_books,
    search_books_by_genre,
)


def main():

    print("=== SEARCH BOOKS ===")

    result = search_books.invoke({"title": "Silent"})

    for book in result[:5]:
        print(book)

    print("\n=== SEARCH BY GENRE ===")

    result = search_books_by_genre.invoke({"genre": "Sci-Fi"})

    print(f"Found: {len(result)} books")

    for book in result[:5]:
        print(book)

    print("\n=== CHECK AVAILABILITY ===")

    if result:
        book_id = result[0]["id"]

        availability = check_availability.invoke({"book_id": book_id})

        print(availability)


if __name__ == "__main__":
    main()
