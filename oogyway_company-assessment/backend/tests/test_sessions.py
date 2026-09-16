import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_session_lifecycle_and_isolation(client: AsyncClient):
    # 1. Create Session A
    res_a = await client.post("/api/v1/sessions", json={"title": "Session A"})
    assert res_a.status_code == 201
    session_a = res_a.json()
    session_a_id = session_a["id"]

    # 2. Create Session B
    res_b = await client.post("/api/v1/sessions", json={"title": "Session B"})
    assert res_b.status_code == 201
    session_b_id = res_b.json()["id"]

    # 3. Post message to Session A
    msg_a = await client.post(
        f"/api/v1/sessions/{session_a_id}/messages",
        json={"content": "What did Brian Chesky say about design?"}
    )
    assert msg_a.status_code == 200

    # 4. Verify Session B has zero messages (Context Isolation)
    msgs_b = await client.get(f"/api/v1/sessions/{session_b_id}/messages")
    assert msgs_b.status_code == 200
    assert len(msgs_b.json()) == 0

    # 5. List sessions
    list_res = await client.get("/api/v1/sessions")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 2

    # 6. Delete Session A
    del_res = await client.delete(f"/api/v1/sessions/{session_a_id}")
    assert del_res.status_code == 204

    # 7. Non-existent session 404 check
    get_404 = await client.get(f"/api/v1/sessions/{session_a_id}")
    assert get_404.status_code == 404
