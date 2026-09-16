import re
from typing import Tuple
from app.services.artifacts.sanitizer import sanitize_html
from app.services.llm.base import LLMProvider


def is_artifact_request(user_prompt: str) -> Tuple[bool, str]:
    """Check if user prompt asks to generate a document/artifact (HTML or Markdown)."""
    p = user_prompt.lower()
    keywords = [
        "generate artifact", "create artifact", "one-pager", "product strategy", 
        "prd", "dashboard", "html page", "write a document", "create a template",
        "turn this into a", "create a page"
    ]
    is_req = any(k in p for k in keywords)
    art_type = "html" if ("html" in p or "dashboard" in p or "page" in p or "css" in p) else "markdown"
    return is_req, art_type


ARTIFACT_SYSTEM_PROMPT = """You are an expert technical designer and product strategist for high-growth startups.
Your task is to generate a complete, professional, standalone artifact based on the user's request.

If generating HTML/CSS:
- Produce clean, modern, fully styled single-file HTML inside standard ```html ... ``` code blocks.
- Use an elegant dark or light glassmorphic UI design system with curated typography, CSS variables, clear card layouts, and responsive grids.
- Do NOT include any `<script>` tags or JavaScript logic. Focus exclusively on visual presentation, typography, and clear layout structure.

If generating Markdown:
- Produce clean, structured Markdown inside standard ```markdown ... ``` code blocks with headings, tables, bullet points, callout blocks, and key takeaways.
"""


async def generate_artifact_content(
    user_prompt: str,
    context: str,
    artifact_type: str,
    llm: LLMProvider
) -> Tuple[str, str, str]:
    """
    Generate artifact title, raw content, and sanitized content.
    """
    prompt = f"User Request: {user_prompt}\n\nRelevant Context:\n{context}\n\nPlease generate a full {artifact_type.upper()} artifact."
    
    raw_response = await llm.generate_response(
        messages=[{"role": "user", "content": prompt}],
        system_prompt=ARTIFACT_SYSTEM_PROMPT
    )

    # Extract block from code fencing if present
    match = re.search(r"```(?:html|markdown|md)?\n(.*?)```", raw_response, re.DOTALL | re.IGNORECASE)
    content = match.group(1).strip() if match else raw_response.strip()

    title = "Product Strategy Document"
    first_line = content.split('\n')[0]
    if first_line.startswith("# ") or "<h1" in first_line:
        title = re.sub(r'<[^>]+>|#\s*', '', first_line).strip()[:60]
    elif "prd" in user_prompt.lower():
        title = "Product Requirements Document (PRD)"
    elif "one-pager" in user_prompt.lower():
        title = "Product Strategy One-Pager"

    sanitized = sanitize_html(content) if artifact_type == "html" else content

    return title, content, sanitized
