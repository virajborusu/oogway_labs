# 2–3 Minute Evaluation Demo Script — The Lenny Growth Assistant

Use this walkthrough script when presenting the live application to evaluators.

---

## ⏱️ Step 1: Introduction (0:00 – 0:30)
> *"Hi everyone! This is **The Lenny Growth Assistant**, a full-stack AI web application designed to help product leaders query grounded insights from Lenny's Podcast and Newsletter transcripts, write long-form Ship 30 for 30 essays, and instantly generate interactive strategy artifacts."*
- Point to the **Model Status Badge** in the top right:
  > *"Notice the status badge showing our active provider: running locally on **Ollama** with `llama3.2`."*

---

## ⏱️ Step 2: Grounded RAG & Source Citations (0:30 – 1:15)
- Click **"Casey Winters PMF"** chip or type:  
  `"What is Casey Winters' mental model for product-market fit?"`
- Press **Enter** / Submit.
- Show response:
  > *"Notice the assistant returns a grounded breakdown emphasizing that retention curves flattening over time is presented in the included Casey Winters fixture as a signal of sustainable product-market fit."*
- Expand the **Grounded Transcript Sources** drawer:
  > *"Every citation comes directly from our PostgreSQL vector knowledge base, showing the guest name, episode title, and exact transcript snippet."*

---

## ⏱️ Step 3: Out-of-Domain Guardrail (1:15 – 1:35)
- Type: `"What is the recipe for baking chocolate chip cookies?"`
- Show response:
  > *"When a query falls outside the knowledge base, the assistant strictly refuses to hallucinate, responding: 'I couldn't find enough relevant material in the Lenny transcript knowledge base to answer that confidently.'"*

---

## ⏱️ Step 4: Ship 30 for 30 Skill (1:35 – 2:10)
- Click **Ship 30 for 30 Skill** chip and submit.
- Show long-form output:
  > *"Here we trigger our specialized **Ship 30 for 30 skill**. Rather than a generic unstructured prompt, this skill executes strict essay writing principles—producing a ~1,250-word structured post with a strong hook, action-oriented headings, selective bolding, and callout takeaways."*

---

## ⏱️ Step 5: Sandboxed Artifact Viewer & XSS Protection (2:10 – 2:45)
- Click **Artifact Generator** chip or type:  
  `"Create an HTML dashboard artifact for PLG conversion metrics."`
- Watch the **Artifact Viewer** slide in on the right:
  > *"The assistant generates a complete HTML dashboard artifact and automatically opens our in-app Artifact Viewer."*
- Toggle between **Preview** and **Source Code**:
  > *"The HTML is rendered inside a strict sandboxed iframe (`sandbox="allow-same-origin"`) with all script tags and inline event handlers sanitized server-side for maximum security."*

---

## ⏱️ Step 6: Conclusion (2:45 – 3:00)
> *"The application is containerized via Docker Compose, includes automated tests covering RAG, sessions, provider routing, Ship 30 for 30, and artifact security, and uses Ollama for the required local demo. Thank you!"*
