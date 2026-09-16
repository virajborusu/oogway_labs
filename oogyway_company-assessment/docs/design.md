# Design & UX Document — The Lenny Growth Assistant

## 1. UX Principles & Information Architecture

The Lenny Growth Assistant interface is designed as a high-density, professional internal productivity tool for product leaders and growth engineers.

### Core Visual Principles
1. **Dark Glassmorphism**: Slate dark background (`#0b0f19`) paired with subtle glass translucent panels (`bg-slate-900/80 backdrop-blur`) and sky accent colors (`#0284c7`).
2. **High Information Density**: Clear visual hierarchy with distinct message bubbles, expandable source accordions, and model status badges.
3. **Dual-Pane Workstation**: Side-by-side chat and Artifact Viewer layout enabling concurrent conversation and document inspection.

---

## 2. Screen & Component Architecture

```
┌────────────────────────────────────────────────────────────────────────────────┐
│  SIDEBAR          │ HEADER (Session Title + Model Badge)                       │
│  ─────────────────┼───────────────────────────────────────────────────────────┤
│  [+ New Session]  │ CHAT MESSAGE STREAM                                       │
│                   │                                                           │
│  Conversations:   │ User: What is Casey Winters' model for retention?         │
│  • PMF & Retention│                                                           │
│  • PLG Strategy   │ Assistant: Retention is the cornerstone...                │
│  • 11-Star Design │ [📚 Grounded Transcript Sources (2)]                      │
│                   │ [📄 Open Generated Artifact Viewer]                       │
│                   │                                                           │
│                   ├───────────────────────────────────────────────────────────┤
│                   │ INPUT BOX                                                 │
│                   │ [Ship 30 Skill] [Artifact Generator] [Send ▶]             │
└───────────────────┴───────────────────────────────────────────────────────────┘
```

---

## 3. Key Interaction Patterns

### A. Grounded Citations Accordion
- Assistant responses include a collapsible **Grounded Transcript Sources** drawer.
- Clicking the drawer expands source cards displaying episode title, guest speaker, relevance match score, and verbatim transcript snippet.

### B. Slide-over Artifact Viewer
- When an artifact (PRD, Strategy One-Pager, HTML Dashboard) is generated, a right-side panel slides in smoothly without interrupting chat flow.
- Users can toggle between **Preview** (rendered HTML/Markdown) and **Source Code** (raw content).
- Includes a 1-click **Copy Code** button.

### C. Provider Status Badge
- Real-time indicator in the header showing the active provider (`OLLAMA`, `ANTHROPIC`, `OPENAI`), target model name (`llama3.2`), and health state (`Online` / `Offline`).

---

## 4. Accessibility & Responsive Design

- **Keyboard Navigation**: Full keyboard accessibility (`Enter` to submit, `Shift+Enter` for multiline text, `Esc` to close artifact viewer).
- **Responsive Layout**: Sidebar collapses cleanly on smaller viewports with touch-friendly targets.
