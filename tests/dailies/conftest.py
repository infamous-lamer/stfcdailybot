import json
from pathlib import Path

import pytest
import responses

from dailies.client import Client

_FIXTURE_EVENTS = json.loads((Path(__file__).parent / "fixtures" / "events_sample.json").read_text())


@pytest.fixture
def mocked_events_api():
    """Mock the events API to return the shared fixture payload; yields the raw JSON."""
    with responses.RequestsMock() as mock:
        mock.add(responses.GET, f"{Client.DEFAULT_API_URL}/api/events", json=_FIXTURE_EVENTS, status=200)
        yield _FIXTURE_EVENTS
