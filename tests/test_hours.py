"""Tests for hours overlap logic."""
from datetime import datetime
from src.utils import hours_overlap, parse_hours


def test_open_at_departure_simple():
    now = datetime(2026, 4, 28, 10, 0)
    departure = datetime(2026, 4, 28, 14, 30)
    assert hours_overlap("06:00-22:00", now, departure) is True


def test_closed_before_now():
    now = datetime(2026, 4, 28, 22, 30)
    departure = datetime(2026, 4, 28, 23, 45)
    assert hours_overlap("06:00-22:00", now, departure) is False


def test_24_hour_lounge():
    now = datetime(2026, 4, 28, 3, 0)
    departure = datetime(2026, 4, 28, 5, 30)
    assert hours_overlap("24h", now, departure) is True


def test_parse_hours_valid():
    result = parse_hours("05:00-22:00")
    assert result is not None
    assert result[0].hour == 5
    assert result[1].hour == 22


def test_parse_hours_invalid():
    assert parse_hours("invalid") is None
