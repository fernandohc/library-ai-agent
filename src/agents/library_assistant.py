import logging
from time import perf_counter
from typing import Literal, NotRequired, TypedDict

from langchain_openai import ChatOpenAI
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from src.agents.analytics_agent import analytics_agent
from src.agents.book_search_agent import book_search_agent
from src.agents.recommendation_agent import recommendation_agent

logger = logging.getLogger(__name__)

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

        self.langfuse_handler = CallbackHandler()
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
        start_time = perf_counter()

        logger.info(
            "Processing library request | question_length=%d",
            len(question),
        )

        try:
            result = self.graph.invoke(
                {"question": question},
                config={
                    "run_name": "library-assistant",
                    "callbacks": [self.langfuse_handler],
                    "tags": ["library-ai-agent", "api"],
                    "metadata": {
                        "application": "library-ai-agent",
                        "input_length": len(question),
                    },
                },
            )

            elapsed_ms = round((perf_counter() - start_time) * 1000, 2)

            logger.info(
                "Library request completed | agent=%s | duration_ms=%s",
                result["agent"],
                elapsed_ms,
            )

            return {
                "agent": result["agent"],
                "answer": result["answer"],
            }

        except Exception:
            elapsed_ms = round((perf_counter() - start_time) * 1000, 2)

            logger.exception(
                "Library request failed | duration_ms=%s",
                elapsed_ms,
            )
            raise
