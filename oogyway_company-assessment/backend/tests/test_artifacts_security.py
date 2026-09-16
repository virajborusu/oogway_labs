import pytest
from httpx import AsyncClient
from app.services.artifacts.sanitizer import sanitize_html


def test_sanitize_html_xss_payloads():
    # 1. Script tag removal
    xss_script = "<div>Hello</div><script>alert('xss')</script>"
    sanitized = sanitize_html(xss_script)
    assert "<script>" not in sanitized.lower()
    assert "alert" not in sanitized.lower()
    assert "<div>Hello</div>" in sanitized

    # 2. Inline event handler (onerror, onclick, onload)
    xss_onerror = '<img src="invalid.jpg" onerror="alert(1)">'
    sanitized_img = sanitize_html(xss_onerror)
    assert "onerror" not in sanitized_img.lower()

    # 3. Javascript protocol URI
    xss_js_link = '<a href="javascript:alert(1)">Click Me</a>'
    sanitized_link = sanitize_html(xss_js_link)
    assert "javascript:" not in sanitized_link.lower()


@pytest.mark.asyncio
async def test_artifact_api_sanitization(client: AsyncClient):
    # Create session
    res_s = await client.post("/api/v1/sessions", json={"title": "Artifact Security Test"})
    session_id = res_s.json()["id"]

    # Post malicious HTML artifact
    malicious_payload = {
        "title": "Malicious Dashboard",
        "artifact_type": "html",
        "content": "<div class='card'><h1>Dashboard</h1><script>document.cookie='stolen'</script><img src=x onerror=alert('hacked')></div>"
    }

    res_art = await client.post(f"/api/v1/sessions/{session_id}/artifacts", json=malicious_payload)
    assert res_art.status_code == 201
    art_data = res_art.json()

    assert "<script>" not in art_data["sanitized_content"].lower()
    assert "onerror" not in art_data["sanitized_content"].lower()
    assert "Dashboard" in art_data["sanitized_content"]
