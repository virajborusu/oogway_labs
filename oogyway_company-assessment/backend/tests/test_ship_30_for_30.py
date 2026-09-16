import pytest
from app.services.skills.ship_30_for_30 import is_ship_30_request, generate_ship_30_essay


def test_is_ship_30_request_detection():
    assert is_ship_30_request("Write a ship 30 for 30 essay on product market fit") is True
    assert is_ship_30_request("Can you write a long-form essay on retention loops?") is True
    assert is_ship_30_request("What is PLG?") is False


@pytest.mark.asyncio
async def test_generate_ship_30_essay():
    class MockLLM:
        provider_name = "test"
        model_name = "test-model"

        async def generate_response(self, messages, system_prompt=None, temperature=0.7, max_tokens=2048):
            return "# Retention Is the Foundation\n\nCasey Winters explains that retention is the foundation of sustainable growth."

    mock_llm = MockLLM()
    sources = [{
        "title": "Casey Winters on Retention",
        "speaker": "Casey Winters",
        "source": "Lenny's Podcast",
        "episode_url": "https://lennysnewsletter.com"
    }]
    essay = await generate_ship_30_essay(
        user_prompt="Write a 30 for 30 essay on retention curves",
        context="Retention curves flattening indicates product market fit.",
        sources=sources,
        llm=mock_llm
    )
    assert len(essay) > 100
    assert "Casey Winters" in essay
