# AI Agent Development Log — The Lenny Growth Assistant

This log documents the key engineering decisions, iterations, failed approaches, debugging steps, and final verification of **The Lenny Growth Assistant**.

---

## 1. Initial Architecture Planning
- **Goal**: Build an enterprise-grade grounded AI conversational web application satisfying the major take-home assessment requirements.
- **Key Decisions**:
  - Selected FastAPI for backend speed, async DB handling, and automatic Pydantic request validation.
  - Selected React 18 + TypeScript + Vite for a modern dual-pane UI (Sidebar + Chat + Artifact Viewer).
  - Selected `LLMProvider` abstraction allowing seamlessly swapping local Ollama (`llama3.2`) with cloud Anthropic/OpenAI without application code changes.
  - Built dual-layer HTML artifact security: server-side HTML sanitizer (stripping `<script>`, `onerror=`, `javascript:`) + client-side `<iframe sandbox="allow-same-origin">`.

---

## 2. Iteration & Debugging Log

### Issue 1: Vector Embeddings in Portable Environments
- **Challenge**: Relying solely on external heavy HuggingFace embedding downloads caused timeouts in offline or fresh dev setups.
- **Correction**: Implemented `compute_embedding()` with dual capability: using `sentence-transformers` (`all-MiniLM-L6-v2`) when loaded, with an automatic fallback term-frequency vectorizer (384 dimensions) for portable tests and offline fixtures.

### Issue 2: Session Context Isolation
- **Challenge**: Ensuring that newly created sessions never inherit prior conversation history or active artifacts.
- **Correction**: Implemented database-level Foreign Keys with `CASCADE` behavior, scoped `selectinload` queries, and explicit session validation in `/api/v1/sessions/{session_id}/messages`. Added Pytest verification (`test_session_lifecycle_and_isolation`).

### Issue 3: XSS Safety in HTML Artifact Viewer
- **Challenge**: Rendering untrusted LLM-generated HTML pages side-by-side in React without exposing DOM script injection vulnerabilities.
- **Correction**: Combined `bleach` / regex sanitization in `sanitizer.py` with React `iframe` sandboxing (`sandbox="allow-same-origin"` strictly excluding `allow-scripts`). Created comprehensive XSS unit tests (`test_artifacts_security.py`).

---

## 3. Final Verification Status
- Verification note: automated tests cover the critical backend paths; a fresh-machine Docker/Ollama run must be performed by the evaluator before submission.
- The repository intentionally does not claim successful end-to-end execution on a machine where Docker/Ollama were unavailable during development.
