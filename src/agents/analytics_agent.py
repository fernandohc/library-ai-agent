from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from src.tools.analytics_tools import (
    get_library_overview,
    get_popular_genres,
    get_top_rated_books,
)

SYSTEM_PROMPT = """
You are an analytics assistant for a library.

Your responsibility is to answer questions about library
statistics using the available tools.

Rules:
- Use the tools to retrieve actual library data.
- Never invent statistics, ratings, or book details.
- Choose the tool that best matches the user's question.
- Clearly distinguish books from physical copies.
- Explain that genre counts represent books associated
  with each genre, not physical copies.
- When presenting top-rated books, include their average
  ratings and rating counts when available.
- If the data does not answer the question, say so clearly.
- Present results in a concise, readable format.
"""

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

analytics_agent = create_agent(
    model=model,
    tools=[
        get_library_overview,
        get_popular_genres,
        get_top_rated_books,
    ],
    system_prompt=SYSTEM_PROMPT,
)
