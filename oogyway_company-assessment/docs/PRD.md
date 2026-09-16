# Product Requirements Document (PRD) — The Lenny Growth Assistant

## 1. Discovery Brief

### User & Problem
Product Managers, Founders, Growth Engineers, and AI Engineers spend significant time searching through hundreds of podcast episodes and newsletter issues for actionable growth frameworks. Existing LLM chatbots hallucinate non-existent quotes, lack source tracing, cannot generate formatted strategy artifacts, and require external tools for long-form writing.

### Job to be Done (JTBD)
*When* I am designing product growth strategies, retention loops, or executive strategy documents,  
*I want to* query transcript knowledge from top product leaders (Brian Chesky, Casey Winters, Elena Verna) with verifiable citations,  
*So that I can* make grounded decisions and instantly generate polished strategy artifacts and Ship 30 for 30 essays.

### Key Pain Points Removed
- **Hallucinated Citations**: Standard LLMs fabricate quotes. The Lenny Assistant provides strict transcript source citations.
- **Unstructured Output**: Generic chats return raw walls of text. The assistant provides an in-app sandboxed Artifact Viewer for HTML/Markdown strategy documents.
- **Lack of Local Privacy**: Cloud-only LLMs expose strategy queries. The system provides first-class Ollama local LLM execution.

### Primary Metrics
- **Grounding Accuracy**: Target: source attribution should be traceable to retrieved transcript chunks; unsupported questions should be refused rather than answered as fact.
- **Source Traceability**: Grounded responses expose retrieved source metadata when available.
- **Artifact Security**: No executable JavaScript should be permitted in rendered artifacts; automated sanitizer tests cover common XSS payloads.

---

## 2. Functional Requirements

### F1: Session & History Management
- System shall allow creating, listing, viewing, and deleting independent chat sessions.
- Context from one session shall never bleed into another session.

### F2: RAG Ingestion & Grounded Retrieval
- System shall ingest transcript files (JSON, TXT, MD), normalize text, split into semantic chunks, and generate vector embeddings.
- Retrieval shall return top-k matching transcript chunks with relevance scores.
- Out-of-domain prompts shall trigger a grounded refusal ("I couldn't find enough relevant material in the Lenny transcript knowledge base to answer that confidently.").

### F3: LLM Provider Abstraction
- System shall support `ollama` (local), `anthropic` (cloud), and `openai` (cloud).
- Provider switching shall be configurable without code modification.
- Active provider status and health shall be displayed in the UI header.

### F4: Ship 30 for 30 Essay Skill
- System shall feature a dedicated skill generating ~1,250 word long-form essays.
- Output must follow Ship 30 writing principles (hook, narrative progression, action-oriented headings, selective bolding, callout takeaways).

### F5: Sandboxed Artifact Generator & Viewer
- System shall generate HTML and Markdown strategy artifacts on request.
- Artifacts shall render in a right-hand slide-over panel with Preview / Source view tabs.
- HTML rendering must be isolated inside `<iframe sandbox="allow-same-origin">` and sanitized against script tags and inline event handlers.

---

## 3. Acceptance Criteria

- [x] FastAPI backend exposes `/health`, `/api/v1/sessions`, `/api/v1/messages`, `/api/v1/artifacts`, `/api/v1/providers/status`.
- [x] Grounded RAG retrieval includes guest name, episode title, and excerpt.
- [x] Out-of-domain questions return explicit non-grounded message without hallucinating sources.
- [x] HTML artifacts strip `<script>` tags, `onerror=`, `onclick=`, and `javascript:` URIs.
- [x] Docker Compose starts all required services with single `docker compose up --build` command.
