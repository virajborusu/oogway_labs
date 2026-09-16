# The Lenny Growth Assistant

A production-grade, grounded AI conversational web application built on **FastAPI**, **React 18**, **PostgreSQL**, **RAG (Retrieval-Augmented Generation)**, local **Ollama** LLMs, a dedicated **Ship 30 for 30 essay writing skill**, and a sandboxed **Artifact Viewer**.

---

## Architecture Overview

```
                          ┌──────────────────────────┐
                          │   React 18 + Vite UI     │
                          │ (Sidebar, Chat, Viewer)  │
                          └─────────────┬────────────┘
                                        │ REST / JSON
                                        ▼
                          ┌──────────────────────────┐
                          │     FastAPI Backend      │
                          └──────┬────────────┬──────┘
                                 │            │
             ┌───────────────────┴──┐      ┌──┴───────────────────┐
             │ RAG Knowledge Base   │      │ LLM Provider Engine  │
             │ (Chunker & Retriever)│      │(Ollama, Anthropic, AI│
             └──────────┬───────────┘      └──────────┬───────────┘
                        │                             │
                        ▼                             ▼
             ┌──────────────────────┐      ┌──────────────────────┐
             │  PostgreSQL Storage  │      │ Ollama (Local LLM)   │
             │(Sessions, Chunks, DB)│      │  http://localhost    │
             └──────────────────────┘      └──────────────────────┘
```

---

## Prerequisites

- **Python**: 3.11 or higher
- **Node.js**: 18.x or higher & `npm`
- **Docker & Docker Compose**: (Optional for containerized setup)
- **Ollama**: (Required for local LLM inference)

---

## Recommended Setup: Docker + Ollama

The assessment demo path is Docker Compose for PostgreSQL/backend/frontend plus Ollama running on the host machine. This avoids requiring you to install PostgreSQL manually.

### 1. Configure environment
Copy `.env.example` to `.env`. On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Leave `LLM_PROVIDER=ollama`. Do not put secrets in Git.

### 2. Install and start Ollama
Install Ollama, open a new PowerShell window, then run:

```powershell
ollama serve
```

In another PowerShell window:

```powershell
ollama pull llama3.2
ollama run llama3.2
```

At the `>>>` prompt, type a test question and press Enter. Type `/bye` to exit the model prompt. Keep `ollama serve` running while the application is running.

### 3. Start the application
From the repository root:

```powershell
docker compose up --build
```

Open:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health

### 4. Ingest the included transcript fixtures
In a second terminal, from the repository root:

```powershell
docker compose exec backend python /scripts/ingest_transcripts.py
```

The repository contains three included transcript fixtures for Brian Chesky, Casey Winters, and Elena Verna. They are demo/test data; add authorized transcript data through the same ingestion pipeline for a larger knowledge base.

### 5. Check provider status
Open:

http://localhost:8000/api/v1/providers/status

The provider should report Ollama and the configured model.

### 6. Stop the application

```powershell
docker compose down
```

Do not use `docker compose down -v` unless you intentionally want to delete the PostgreSQL data volume.

## Alternative: Local Backend/Frontend Development

The repository can also be developed without the application containers, but PostgreSQL is still required for the intended deployment configuration. Python 3.11+ is required. The Docker path above is recommended for the assessment because it is reproducible and avoids local database setup.

## Key Features

1. **Grounded RAG Knowledge Base**:
   - Ingests the included Lenny transcript fixtures (Brian Chesky, Casey Winters, Elena Verna) and supports additional TXT, Markdown, and JSON transcript files through the ingestion pipeline.
   - Preserves source title, guest speaker, source identifier, and retrieved snippets.
   - Refuses out-of-domain questions cleanly ("I couldn't find enough relevant material in the Lenny transcript knowledge base to answer that confidently.").

2. **LLM Provider Abstraction**:
   - Seamlessly switch between **Ollama (Local)**, **Anthropic Claude**, and **OpenAI**.
   - Real-time provider health checking and descriptive error reporting.

3. **Ship 30 for 30 Skill**:
   - Specialized long-form essay generator (~1,250 words) adhering to Ship 30 writing principles (strong hook, narrative arc, headings, selective bolding, grounded takeaways).

4. **In-App Sandboxed Artifact Viewer**:
   - Generates HTML and Markdown artifacts (PRDs, Strategy One-Pagers, Dashboards).
   - Rendered in a right-hand slide-over panel beside the chat.
   - HTML is sanitized and isolated inside `<iframe sandbox="allow-same-origin">` to block XSS execution.

---

## Running Tests

### Backend Test Suite (Pytest)
```bash
cd backend
pytest -v
```

### Run Security & XSS Tests Specifically
```bash
cd backend
pytest tests/test_artifacts_security.py -v
```

---

## Documentation

- [PRD.md](docs/PRD.md): Product requirements & acceptance criteria
- [design.md](docs/design.md): UX principles, information architecture, component design
- [architecture.md](docs/architecture.md): Technical architecture & diagrams
- [manual-test-plan.md](docs/manual-test-plan.md): 13-step QA checklist
- [demo-script.md](docs/demo-script.md): 2-3 minute presentation script
- [agent development log](agent-transcripts/development_log.md): AI agent engineering decisions

## Fresh-Machine Verification Checklist

From a fresh checkout, verify the following in order:

```powershell
docker --version
docker compose version
ollama --version
ollama list
```

Then:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

In a second terminal:

```powershell
docker compose exec backend python /scripts/ingest_transcripts.py
docker compose exec backend pytest -q
```

Finally open `http://localhost:3000` and complete the manual test plan in `docs/manual-test-plan.md`.
