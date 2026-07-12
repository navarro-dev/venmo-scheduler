import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from venmo_api import PaymentStatus

from utilities.util import is_request_sent, month_year_date


def make_request(
    username="testuser",
    amount=10.0,
    note="rent",
    status=PaymentStatus.PENDING,
    year=2026,
    month=7,
    day=1,
):
    req = MagicMock()
    req.target.username = username
    req.amount = amount
    req.note = note
    req.status = status
    req.date_created = datetime(year, month, day).timestamp()
    return req


class TestMonthYearDate:
    def test_returns_month_and_year(self):
        assert month_year_date(datetime(2026, 7, 11)) == "July 2026"

    def test_same_month_different_days_match(self):
        assert month_year_date(datetime(2026, 7, 1)) == month_year_date(datetime(2026, 7, 31))

    def test_different_months_do_not_match(self):
        assert month_year_date(datetime(2026, 7, 1)) != month_year_date(datetime(2026, 8, 1))

    def test_different_years_do_not_match(self):
        assert month_year_date(datetime(2025, 7, 1)) != month_year_date(datetime(2026, 7, 1))


class TestIsRequestSent:
    def test_matching_request_returns_true(self):
        req = make_request(username="alice", amount=10.0, note="rent")
        assert is_request_sent("alice", 10.0, "rent", [req]) is True

    def test_empty_list_returns_false(self):
        assert is_request_sent("alice", 10.0, "rent", []) is False

    def test_different_username_returns_false(self):
        req = make_request(username="bob")
        assert is_request_sent("alice", 10.0, "rent", [req]) is False

    def test_different_amount_returns_false(self):
        req = make_request(amount=10.0)
        assert is_request_sent("testuser", 20.0, "rent", [req]) is False

    def test_different_note_returns_false(self):
        req = make_request(note="rent")
        assert is_request_sent("testuser", 10.0, "utilities", [req]) is False

    def test_cancelled_status_returns_false(self):
        req = make_request(status=PaymentStatus.CANCELLED)
        assert is_request_sent("testuser", 10.0, "rent", [req]) is False

    def test_settled_status_returns_true(self):
        req = make_request(status=PaymentStatus.SETTLED)
        assert is_request_sent("testuser", 10.0, "rent", [req]) is True

    def test_pending_status_returns_true(self):
        req = make_request(status=PaymentStatus.PENDING)
        assert is_request_sent("testuser", 10.0, "rent", [req]) is True

    def test_different_month_returns_false(self):
        req = make_request(year=2026, month=6, day=1)
        with patch("utilities.util.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 7, 11)
            mock_dt.fromtimestamp.side_effect = datetime.fromtimestamp
            assert is_request_sent("testuser", 10.0, "rent", [req]) is False

    def test_same_month_different_day_returns_true(self):
        req = make_request(year=2026, month=7, day=1)
        with patch("utilities.util.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 7, 11)
            mock_dt.fromtimestamp.side_effect = datetime.fromtimestamp
            assert is_request_sent("testuser", 10.0, "rent", [req]) is True

    def test_first_match_short_circuits(self):
        requests = [
            make_request(username="other"),
            make_request(username="testuser"),
            make_request(username="testuser"),
        ]
        assert is_request_sent("testuser", 10.0, "rent", requests) is True
