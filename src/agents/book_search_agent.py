from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from src.tools.book_tools import (
    check_availability,
    get_book,
    search_available_books_by_genre,
    search_books,
    search_books_by_author,
    search_books_by_genre,
)

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)


SYSTEM_PROMPT = """
You are a library assistant specialized in helping users find books.

You have access to tools that allow you to search the library catalog
and check book availability.

Rules:

1. Use the available tools whenever the user's question requires
   information from the library database.

2. Never invent books, authors, ratings, genres, or availability.

3. If the requested information cannot be found, clearly say that
   the information was not found.

4. When searching for books by genre, use the genre search tool.

5. When the user asks whether a specific book is available,
   use the availability tool.

6. Keep responses concise and useful.

7. When presenting books, include the title and relevant information
   such as author, genre, and rating when available.
"""


book_search_agent = create_agent(
    model=model,
    tools=[
        search_books,
        search_available_books_by_genre,
        get_book,
        search_books_by_genre,
        search_books_by_author,
        check_availability,
    ],
    system_prompt=SYSTEM_PROMPT,
)
