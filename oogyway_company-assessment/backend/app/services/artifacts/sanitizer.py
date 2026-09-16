import re

try:
    import bleach
    HAS_BLEACH = True
except ImportError:
    HAS_BLEACH = False


ALLOWED_TAGS = [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'span', 'b', 'i', 'strong',
    'em', 'u', 's', 'strike', 'blockquote', 'code', 'pre', 'ul', 'ol', 'li',
    'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td', 'a', 'img', 'hr',
    'br', 'style', 'section', 'article', 'main', 'header', 'footer', 'nav'
]

ALLOWED_ATTRIBUTES = {
    '*': ['class', 'style', 'id', 'title'],
    'a': ['href', 'target', 'rel'],
    'img': ['src', 'alt', 'width', 'height'],
    'td': ['colspan', 'rowspan'],
    'th': ['colspan', 'rowspan']
}


def sanitize_html(raw_html: str) -> str:
    """
    Sanitize untrusted HTML artifacts.
    Strips scripts, inline JS handlers (onload, onerror, onclick), dangerous protocols (javascript:), and forms.
    """
    if not raw_html:
        return ""

    cleaned = raw_html

    # Remove <script> tags completely
    cleaned = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', cleaned, flags=re.IGNORECASE)

    # Remove inline event attributes like onerror=, onclick=, onload=, etc.
    cleaned = re.sub(r'\s+on[a-z]+\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+)', '', cleaned, flags=re.IGNORECASE)

    # Remove javascript: URIs in href or src
    cleaned = re.sub(r'(href|src)\s*=\s*["\']?\s*javascript:[^"\'>\s]+["\']?', '', cleaned, flags=re.IGNORECASE)

    # Remove <form>, <input>, <iframe capabilities if injected>
    cleaned = re.sub(r'<\/?(form|input|button|textarea|select|option)\b[^>]*>', '', cleaned, flags=re.IGNORECASE)

    if HAS_BLEACH:
        try:
            cleaned = bleach.clean(
                cleaned,
                tags=ALLOWED_TAGS,
                attributes=ALLOWED_ATTRIBUTES,
                strip=True
            )
        except Exception:
            pass

    return cleaned.strip()
