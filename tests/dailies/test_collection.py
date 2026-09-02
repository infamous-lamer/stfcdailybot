from datetime import UTC, datetime

from dailies.collection import EventCollection
from dailies.event import Event


def _event(id, start, end, category="daily", active=True, **overrides):
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
        "eventCategory": category,
        "priority": "normal",
        "minOpsLevel": None,
        "maxOpsLevel": None,
        "repeatType": "none",
        "repeatConfig": None,
        "isActive": active,
        "createdAt": start,
        "updatedAt": start,
    }
    data.update(overrides)
    return Event.model_validate(data)


EVENT_A = _event(1, "2026-06-05T16:00:00Z", "2026-06-06T16:00:00Z", category="daily", priority="arc")
EVENT_B = _event(2, "2026-06-04T16:00:00Z", "2026-06-05T16:00:00Z", category="weekly", priority="normal")
EVENT_C = _event(
    3, "2026-06-04T16:00:00Z", "2026-06-11T16:00:00Z", category="daily", active=False, priority="incursion"
)
EVENT_D = _event(4, "2026-06-06T16:00:00Z", "2026-06-07T16:00:00Z", category="monthly", priority="normal")


def test_collection_is_sorted_by_start_time_regardless_of_input_order():
    collection = EventCollection([EVENT_A, EVENT_D, EVENT_B, EVENT_C])

    assert [e.id for e in collection] == [2, 3, 1, 4]


def test_len_and_indexing():
    collection = EventCollection([EVENT_A, EVENT_B])

    assert len(collection) == 2
    assert collection[0] is EVENT_B
    assert collection[1] is EVENT_A


def test_by_category_filters_exact_match():
    collection = EventCollection([EVENT_A, EVENT_B, EVENT_C, EVENT_D])

    daily = collection.by_category("daily")

    assert [e.id for e in daily] == [3, 1]


def test_by_active_filters_on_is_active_flag():
    collection = EventCollection([EVENT_A, EVENT_B, EVENT_C, EVENT_D])

    assert [e.id for e in collection.by_active(True)] == [2, 1, 4]
    assert [e.id for e in collection.by_active(False)] == [3]


def test_by_priority_filters_exact_match():
    collection = EventCollection([EVENT_A, EVENT_B, EVENT_C, EVENT_D])

    assert [e.id for e in collection.by_priority("normal")] == [2, 4]
    assert [e.id for e in collection.by_priority("arc")] == [1]
    assert [e.id for e in collection.by_priority("incursion")] == [3]


def test_at_returns_events_covering_the_given_instant():
    collection = EventCollection([EVENT_A, EVENT_B, EVENT_C, EVENT_D])

    # 2026-06-08: only C (spanning 06-04 to 06-11) is still active; A, B,
    # and D have all already ended by this point.
    moment = datetime(2026, 6, 8, 0, 0, tzinfo=UTC)
    active = collection.at(moment)

    assert [e.id for e in active] == [3]


def test_at_boundary_is_start_inclusive_end_exclusive():
    collection = EventCollection([EVENT_A, EVENT_B])

    start_of_b = datetime(2026, 6, 4, 16, 0, tzinfo=UTC)
    end_of_b = datetime(2026, 6, 5, 16, 0, tzinfo=UTC)

    assert [e.id for e in collection.at(start_of_b)] == [2]
    assert [e.id for e in collection.at(end_of_b)] == [1]


def test_filters_are_chainable():
    collection = EventCollection([EVENT_A, EVENT_B, EVENT_C, EVENT_D])

    result = collection.by_category("daily").by_active(False)
    assert [e.id for e in result] == [3]

    result = collection.by_category("daily").by_priority("incursion")
    assert [e.id for e in result] == [3]


def test_start_times_and_end_times_are_unique_and_sorted():
    collection = EventCollection([EVENT_A, EVENT_B, EVENT_C, EVENT_D])

    assert collection.start_times == [
        datetime(2026, 6, 4, 16, 0, tzinfo=UTC),
        datetime(2026, 6, 5, 16, 0, tzinfo=UTC),
        datetime(2026, 6, 6, 16, 0, tzinfo=UTC),
    ]
    assert collection.end_times == [
        datetime(2026, 6, 5, 16, 0, tzinfo=UTC),
        datetime(2026, 6, 6, 16, 0, tzinfo=UTC),
        datetime(2026, 6, 7, 16, 0, tzinfo=UTC),
        datetime(2026, 6, 11, 16, 0, tzinfo=UTC),
    ]


def test_empty_collection():
    collection = EventCollection([])

    assert len(collection) == 0
    assert list(collection) == []
    assert collection.start_times == []
    assert collection.end_times == []


def test_fetch_parses_all_records(mocked_events_api):
    collection = EventCollection.fetch()

    assert len(collection) == len(mocked_events_api)
    assert all(isinstance(e, Event) for e in collection)


def test_fetch_timestamps_are_parsed_as_utc_datetimes(mocked_events_api):
    event = next(e for e in EventCollection.fetch() if e.id == 199)

    assert event.start_time == datetime(2026, 6, 4, 16, 0, tzinfo=UTC)
    assert event.end_time == datetime(2026, 6, 5, 16, 0, tzinfo=UTC)
    assert event.title == "Academy System - SLB"
    assert event.event_category == "daily"
    assert event.event_format == "SLB"
    assert event.min_ops_level == 61


def test_fetch_nullable_fields_pass_through_as_none(mocked_events_api):
    incursion = next(e for e in EventCollection.fetch() if e.id == 279)

    assert incursion.event_format is None
    assert incursion.event_category == "none"
    assert incursion.max_ops_level is None
    assert incursion.repeat_config is None


def test_fetch_repeat_config_is_preserved_as_a_dict(mocked_events_api):
    event = next(e for e in EventCollection.fetch() if e.id == 580)

    assert event.repeat_type == "weekly"
    assert event.repeat_config == {"interval": 1, "daysOfWeek": "2"}


def test_fetch_null_description_is_allowed(mocked_events_api):
    event = next(e for e in EventCollection.fetch() if e.id == 271)

    assert event.description is None


def test_fetch_then_by_category_filters_daily_events(mocked_events_api):
    daily = EventCollection.fetch().by_category("daily")

    assert len(daily) == 1
    assert daily[0].id == 199
