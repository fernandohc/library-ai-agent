# Library AI Agent

An AI-powered library assistant built with **Python, LangChain, LangGraph, FastAPI, and MongoDB**. The application routes a user's question to a specialized agent that searches the book catalog, recommends books based on a user's borrowing history, or answers library analytics questions.

> This is a portfolio and learning project. The database is populated with synthetic sample data. The default MongoDB credentials are for local development only and must not be reused in a production deployment.

## Features

- **Book search agent** — search by title, author, or genre; retrieve book details; check copy availability.
- **Recommendation agent** — recommend books using a user's borrowing history and ratings.
- **Analytics agent** — retrieve library overview statistics, popular genres, and top-rated books.
- **LangGraph orchestration** — route each question to the appropriate specialized agent.
- **FastAPI** — expose the assistant through an HTTP API with request validation.
- **MongoDB** — persist books, authors, users, physical copies, reviews, and loan history.
- **Docker Compose** — run the API and database locally.

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
  +--> Book Search Agent ------+
  +--> Recommendation Agent ---+--> LangChain tools --> Services --> Repositories --> MongoDB
  +--> Analytics Agent --------+
```

The agents use `gpt-4o-mini` through the OpenAI API. Tools retrieve application data from MongoDB; the language model is instructed not to invent catalog details or statistics.

## Tech stack

- Python 3.12
- FastAPI and Uvicorn
- LangChain and LangGraph
- OpenAI API (`gpt-4o-mini`)
- MongoDB 8 and PyMongo
- Pydantic
- Docker Compose
- Pytest and HTTPX

## Prerequisites

- Docker Desktop with Docker Compose
- Python 3.12+ (for running the seed script and tests on the host)
- An OpenAI API key with API access enabled

## Run locally with Docker

### 1. Configure environment variables

Copy the example environment file and add your OpenAI API key:

**PowerShell**

```powershell
Copy-Item .env.example .env
notepad .env
```

Replace `your_openai_api_key_here` with your key. Do not commit `.env` to Git.

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

The seed script generates synthetic authors, books, users, book copies, reviews, and loan history. **Running it again clears and recreates the project's collections**, so do not run it against data you need to preserve.

### 5. Start the API

```powershell
docker compose up -d --build library-api
```

The API is available at `http://localhost:8000`.

- Interactive API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

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

## Run tests

Activate the virtual environment, then run:

```powershell
python -m pytest tests -v
```

The API tests use a fake assistant, so they validate the HTTP contract without making OpenAI API calls or requiring live database queries.

## Useful commands

```powershell
# View service status
docker compose ps

# Follow API logs
docker compose logs -f library-api

# Follow MongoDB logs
docker compose logs -f mongodb

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

## Current limitations

- The project exposes an HTTP API; it does not include a frontend.
- The sample dataset is synthetic and intended for demonstration.
- The API's `/ask` endpoint returns a generic HTTP 500 response if request processing fails; details are available in the application logs.
- Dependency versions are currently declared without strict pins in `requirements.txt`; a lock or pinned dependency file can be added after validating the target environment.

## License

No license has been added yet. If you want others to reuse, modify, or distribute the project, choose a license and add a `LICENSE` file before publishing.
