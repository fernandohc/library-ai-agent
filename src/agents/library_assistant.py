from typing import Literal, NotRequired, TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from src.agents.analytics_agent import analytics_agent
from src.agents.book_search_agent import book_search_agent
from src.agents.recommendation_agent import recommendation_agent

AgentName = Literal[
    "book_search",
    "recommendation",
    "analytics",
]


class LibraryState(TypedDict):
    question: str
    agent: NotRequired[AgentName]
    answer: NotRequired[str]


class RoutingDecision(BaseModel):
    agent: AgentName = Field(
        description="The agent best suited to answer the user's request."
    )


class LibraryAssistant:
    def __init__(self):
        self.router_model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
        ).with_structured_output(RoutingDecision)

        self.graph = self._build_graph()

    def _route_request(self, state: LibraryState) -> dict:
        decision = self.router_model.invoke(
            [
                (
                    "system",
                    """
                Classify the user's request into exactly one category.

                book_search:
                Search books, find books by genre or author,
                retrieve book details, or check availability.

                recommendation:
                Recommend books personalized to a user's
                borrowing history and ratings.

                analytics:
                Answer questions about library statistics,
                genre distribution, and top-rated books.

                Choose the category that best matches the
                user's main intent.
                """,
                ),
                ("human", state["question"]),
            ]
        )

        return {"agent": decision.agent}

    def _run_book_search(self, state: LibraryState) -> dict:
        result = book_search_agent.invoke(
            {"messages": [{"role": "user", "content": state["question"]}]}
        )

        return {"answer": result["messages"][-1].content}

    def _run_recommendation(self, state: LibraryState) -> dict:
        result = recommendation_agent.invoke(
            {"messages": [{"role": "user", "content": state["question"]}]}
        )

        return {"answer": result["messages"][-1].content}

    def _run_analytics(self, state: LibraryState) -> dict:
        result = analytics_agent.invoke(
            {"messages": [{"role": "user", "content": state["question"]}]}
        )

        return {"answer": result["messages"][-1].content}

    def _build_graph(self):
        builder = StateGraph(LibraryState)

        builder.add_node("router", self._route_request)
        builder.add_node("book_search", self._run_book_search)
        builder.add_node("recommendation", self._run_recommendation)
        builder.add_node("analytics", self._run_analytics)

        builder.add_edge(START, "router")

        builder.add_conditional_edges(
            "router",
            lambda state: state["agent"],
            {
                "book_search": "book_search",
                "recommendation": "recommendation",
                "analytics": "analytics",
            },
        )

        builder.add_edge("book_search", END)
        builder.add_edge("recommendation", END)
        builder.add_edge("analytics", END)

        return builder.compile()

    def ask(self, question: str) -> dict:
        result = self.graph.invoke({"question": question})

        return {
            "agent": result["agent"],
            "answer": result["answer"],
        }
