from langchain_core.tools import tool

from src.container import get_container


@tool
def get_user_loan_history(user_id: str) -> list[dict]:
    """
    Get the borrowing history of a library user.

    Use this tool when you need to understand which books
    a user has previously borrowed.
    """

    history = get_container().user_service.get_loan_history(user_id)

    return history
