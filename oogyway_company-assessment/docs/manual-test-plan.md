# Manual Test Plan — The Lenny Growth Assistant

Use this test plan to manually verify all 13 core user flows before submitting or demonstrating the project.

---

## Verification Flow Matrix

| Flow | Description | Step-by-Step Instructions | Expected Result | Pass/Fail |
| :--- | :--- | :--- | :--- | :---: |
| **Flow A** | Create New Chat | Click `+ New Growth Session` in sidebar | New empty session created, active in list, input cleared | [ ] |
| **Flow B** | Ask Grounded Question | Ask: *"What did Brian Chesky say about experience design?"* | Assistant returns answer citing Brian Chesky and 11-star design | [ ] |
| **Flow C** | Ask Follow-up Question | Ask: *"How can I apply this 11-star concept to SaaS?"* | Assistant preserves session context and provides follow-up | [ ] |
| **Flow D** | Inspect Sources | Click `Grounded Transcript Sources` drawer under response | Drawer opens showing guest name, episode title, and excerpt | [ ] |
| **Flow E** | Out-of-Domain Refusal | Ask: *"What is the recipe for baking chocolate cake?"* | Assistant returns: *"I couldn't find enough relevant material..."* | [ ] |
| **Flow F** | Ship 30 for 30 Essay | Click `Ship 30 for 30 Skill` chip and submit | Generates ~1,250-word essay with hook, headings, bolding & takeaways | [ ] |
| **Flow G** | Markdown Artifact | Ask: *"Create a PRD markdown artifact for feature flags"* | Artifact Viewer opens on right showing formatted Markdown PRD | [ ] |
| **Flow H** | HTML/CSS Artifact | Ask: *"Generate an HTML dashboard artifact for retention metrics"* | Artifact Viewer opens rendering styled HTML preview | [ ] |
| **Flow I** | Artifact Source View | Click `Source Code` tab in Artifact Viewer | Displays raw HTML/Markdown source code with Copy button | [ ] |
| **Flow J** | Security XSS Test | Try sending: `<script>alert('xss')</script>` in artifact prompt | HTML is sanitized and rendered inside sandboxed iframe without alert | [ ] |
| **Flow K** | Provider Health | Check header status badge | Displays active provider (`ollama`), model (`llama3.2`), and health status | [ ] |
| **Flow L** | Local Ollama Execution | Ensure Ollama is running (`ollama serve`) | Responses are generated locally via Ollama | [ ] |
| **Flow M** | Session Persistence | Refresh browser page | Previous sessions and conversation history remain intact | [ ] |
