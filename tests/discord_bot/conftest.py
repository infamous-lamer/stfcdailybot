import pytest

from dailies.event import Event


def _make_event(id, start, end, **overrides):
    data = {
        "id": id,
        "title": f"Event {id}",
        "description": None,
        "imageUrl": None,
        "startTime": start,
        "endTime": end,
        "eventType": "hostiles",
        "eventSubType": None,
        "eventFormat": None,
        "eventCategory": "daily",
        "priority": "normal",
        "minOpsLevel": None,
        "maxOpsLevel": None,
        "repeatType": "none",
        "repeatConfig": None,
        "isActive": True,
        "createdAt": start,
        "updatedAt": start,
    }
    data.update(overrides)
    return Event.model_validate(data)


@pytest.fixture
def event_factory():
    """Factory fixture building synthetic `Event`s for tests, e.g. `event_factory(1, start, end)`."""
    return _make_event
