from dailies.client import Client


def test_fetch_events_returns_raw_json(mocked_events_api):
    events = Client().fetch_events()

    assert events == mocked_events_api
