import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request

from src.agents.library_assistant import LibraryAssistant
from src.container import close_container
from src.schemas.chat import AskRequest, AskResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Library AI Assistant")

    app.state.assistant = LibraryAssistant()

    try:
        yield
    finally:
        logger.info("Shutting down Library AI Assistant")
        close_container()


app = FastAPI(
    title="Library AI Assistant",
    description=(
        "API for book search, personalized recommendations, and library analytics."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "application": "library-ai-agent",
    }


@app.post("/ask", response_model=AskResponse)
def ask_library(
    payload: AskRequest,
    request: Request,
) -> AskResponse:
    assistant = request.app.state.assistant

    try:
        result = assistant.ask(payload.question)

        return AskResponse(
            agent=result["agent"],
            answer=result["answer"],
        )

    except Exception:
        logger.exception("Failed to process library question")

        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the question.",
        )
