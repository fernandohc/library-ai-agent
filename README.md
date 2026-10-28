# Library AI Agent

An AI-powered library assistant built with **Python, LangChain, LangGraph, FastAPI, and MongoDB**. The application routes a user's question to a specialized agent that searches the book catalog, recommends books based on a user's borrowing history, or answers library analytics questions.

> This is a portfolio and learning project. The database is populated with synthetic sample data. The default MongoDB credentials are for local development only and must not be reused in a production deployment.

## Features

- **Book search agent** — search by title, author, or genre; retrieve book details; check copy availability.
- **Recommendation agent** — recommend books using a user's borrowing history and ratings.
- **Analytics agent** — retrieve library overview statistics, popular genres, and top-rated books.
- **LangGraph orchestration** — route each question to the appropriate specialized agent.
- **LangChain tools** — expose catalog searches, availability checks, recommendations, and analytics operations to the agents.
- **Direct tool responses** — return formatted results directly for selected queries, avoiding unnecessary LLM calls when additional language generation is not needed.
- **FastAPI** — expose the assistant through an HTTP API with request validation.
- **MongoDB** — persist books, authors, users, physical copies, reviews, and loan history.
- **Langfuse observability** — trace agent execution, LLM calls, tool invocations, latency, token usage, and costs.
- **Application logging** — record request processing, selected agents, execution duration, and exceptions.
- **Docker Compose** — run the API and database locally.
- **Pytest** — automate application and API tests.

## Architecture

```text
Client
  |
  v
FastAPI (/ask)
  |
  v
LibraryAssistant (LangGraph)
  |
  +--> Router (LLM)
  |       |
  |       +--> Book Search Agent
  |       +--> Recommendation Agent
  |       +--> Analytics Agent
  |
  +--> LangChain tools
          |
          v
       Services
          |
          v
       Repositories
          |
          v
        MongoDB

Observability:
  LibraryAssistant --> Langfuse
  Application logs --> Python logging
```

The agents use `gpt-4o-mini` through the OpenAI API. LangGraph orchestrates the workflow, while the router uses structured output to select the appropriate agent.

LangChain tools retrieve application data from MongoDB. The language model is instructed not to invent catalog details or statistics.

The `search_available_books_by_genre` tool uses `return_direct=True` and formats its results in Python. This allows the book search agent to return the result without an additional LLM generation step for that query.

The MongoDB aggregation for this operation projects only the fields required by the response, reducing unnecessary data returned from the database.

## Observability with Langfuse

The application integrates Langfuse through the LangChain callback handler.

Traces can be used to inspect:

- The overall `library-assistant` execution.
- The router's LLM invocation and selected agent.
- Agent execution and nested model calls.
- Tool inputs, outputs, and execution durations.
- LLM latency, token usage, and estimated cost when available.

The application also records basic operational events using Python's `logging` module:

- Request processing starts, including the question length.
- Successful completion, including the selected agent and elapsed time.
- Exceptions, including stack traces and elapsed time.

The question text itself is not included in the custom start log. However, Langfuse tracing may capture prompts and tool inputs or outputs. Review your data-handling requirements before using real user data.

### Configure Langfuse

Create a Langfuse project and obtain its public and secret keys. Configure the following variables in `.env`:

```dotenv
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_BASE_URL=https://cloud.langfuse.com
LANGFUSE_TRACING_ENVIRONMENT=development
```

The base URL should match your Langfuse deployment. For a self-hosted instance, use the URL of that instance.

The application passes the callback handler to LangGraph and attaches run metadata, including the application name, request input length, and tags.

After starting the API and sending a request to `/ask`, open Langfuse and navigate to **Tracing** to inspect the execution.

For performance comparisons, use the same question and compare total trace duration, individual model-call durations, token usage, and cost. A reduction in the number of LLM calls does not guarantee a proportional reduction in total latency, because routing, database access, and other processing still contribute to execution time.

## Tech stack

- Python 3.12
- FastAPI and Uvicorn
- LangChain and LangGraph
- OpenAI API (`gpt-4o-mini`)
- Langfuse
- MongoDB 8 and PyMongo
- Pydantic
- Docker Compose
- Pytest and HTTPX

## Prerequisites

- Docker Desktop with Docker Compose
- Python 3.12+ (for running the seed script and tests on the host)
- An OpenAI API key with API access enabled
- A Langfuse project and API keys for tracing

## Run locally with Docker

### 1. Configure environment variables

Copy the example environment file and add your OpenAI API key and Langfuse credentials:

**PowerShell**

```powershell
Copy-Item .env.example .env
notepad .env
```

Set `OPENAI_API_KEY`, `LANGFUSE_PUBLIC_KEY`, and `LANGFUSE_SECRET_KEY`. Verify `LANGFUSE_BASE_URL` and `LANGFUSE_TRACING_ENVIRONMENT` are correct for your environment.

Do not commit `.env` to Git.

### 2. Start MongoDB

```powershell
docker compose up -d mongodb
```

Wait until MongoDB is healthy:

```powershell
docker compose ps
```

### 3. Create a Python environment and install dependencies

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Seed the database

```powershell
python -m scripts.seed
```

The seed script generates synthetic authors, books, users, book copies, reviews, and loan history.

**Running the seed script again clears and recreates the project's collections.** Do not run it against data you need to preserve.

### 5. Start the API

```powershell
docker compose up -d --build library-api
```

The API is available at `http://localhost:8000`.

- Interactive API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health check: [http://localhost:8000/health](http://localhost:8000/health)

The Docker Compose configuration passes the OpenAI and Langfuse environment variables to the API container.

## API usage

### Health check

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "application": "library-ai-agent"
}
```

### Ask the assistant

```http
POST /ask
Content-Type: application/json
```

Example request:

```json
{
  "question": "Which horror books are currently available?"
}
```

Example response shape:

```json
{
  "agent": "book_search",
  "answer": "..."
}
```

You can also try questions such as:

- `Find books by the author author-001.`
- `Recommend five books for user-001.`
- `Which genres have the most books?`
- `What are the top-rated books in the library?`

The exact answer depends on the generated sample data. Requests to `/ask` require a working OpenAI API key and a reachable MongoDB instance.

## Performance and observability considerations

The project includes a direct-response optimization for the available-books-by-genre tool.

Instead of returning raw records to the agent for another LLM call to format, the tool formats the result in Python and returns it directly. The corresponding MongoDB aggregation also limits its projection to the fields required by the response.

During development, a measured execution for one query decreased from approximately **11.65 seconds to 2.99 seconds** after the direct-response optimization. This is an observation from a single comparison, not a general performance guarantee. Actual results depend on the question, model latency, database state, and execution environment.

The Langfuse traces help identify where time is spent across routing, agent execution, model calls, and tools. Application logs complement these traces by capturing operational events and exceptions.

## Run tests

Activate the virtual environment, then run:

```powershell
python -m pytest tests -v
```

The API tests use a fake assistant, so they validate the HTTP contract without making OpenAI API calls or requiring live database queries.

Some scripts and tests may require a configured database or other environment variables. Check each script's setup before running it.

## Useful commands

```powershell
# View service status
docker compose ps

# Follow API logs
docker compose logs -f library-api

# Follow MongoDB logs
docker compose logs -f mongodb

# Rebuild and start the API
docker compose up -d --build library-api

# Stop services (database volume is preserved)
docker compose down

# Stop services and delete the local database volume
# WARNING: this permanently deletes the local MongoDB data.
docker compose down -v
```

## Project structure

```text
src/
  agents/        # Specialized agents and LangGraph orchestration
  database/      # MongoDB connection
  models/        # Pydantic domain models
  repositories/  # MongoDB data access
  schemas/       # API request and response schemas
  services/      # Application and business logic
  tools/         # Tools exposed to LangChain agents
  api.py         # FastAPI application
  container.py   # Dependency composition

scripts/         # Seed data and manual smoke-test scripts
tests/           # Automated tests

docker/
  mongodb/       # MongoDB initialization script

Dockerfile
docker-compose.yml
requirements.txt
.env.example
```

## Security notes

- Never commit `.env`, API keys, passwords, or production data.
- The MongoDB credentials in the local Docker configuration are development defaults, not production credentials.
- Do not expose this development setup publicly without configuring secrets, authentication, network access, and appropriate operational safeguards.
- Avoid sending sensitive personal information, credentials, or confidential data to LLM providers or observability platforms unless the relevant privacy and security requirements have been reviewed.
- Review Langfuse trace retention and access controls, as traces may contain prompts, model outputs, tool inputs, and tool outputs.
- Keep observability failures from interrupting application requests where possible, and configure appropriate monitoring and alerting for a production deployment.

## Current limitations

- The project exposes an HTTP API; it does not include a frontend.
- The sample dataset is synthetic and intended for demonstration.
- The API's `/ask` endpoint returns a generic HTTP 500 response if request processing fails; details are available in the application logs.
- Langfuse provides LLM and agent observability but does not replace comprehensive infrastructure monitoring, centralized application logging, or API metrics.
- The direct-response optimization is implemented for the available-books-by-genre tool. Other tools may still require additional LLM processing.
- Dependency versions are currently declared without strict pins in `requirements.txt`; a lock or pinned dependency file can be added after validating the target environment.

## License

No license has been added yet. If you want others to reuse, modify, or distribute the project, choose a license and add a `LICENSE` file before publishing.
