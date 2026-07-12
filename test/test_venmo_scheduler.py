import pytest
from unittest.mock import MagicMock, patch

from venmo_scheduler import venmo_scheduler as scheduler


def make_venmo_mock(username="testuser"):
    mock_venmo = MagicMock()
    mock_user = MagicMock()
    mock_user.username = username
    mock_venmo._validate_user.return_value = mock_user
    mock_venmo._get_charge_payments.return_value = []
    return mock_venmo


ENV_BASE = {
    "ACCESS_TOKEN": "token123",
    "REQUEST_USERS": "testuser",
    "REQUEST_AMOUNT": "10.0",
    "REQUEST_NOTE": "rent",
    "SEND_REQUEST": "FALSE",
}


class TestInputValidation:
    def test_missing_access_token_returns_400(self, monkeypatch):
        for k, v in {**ENV_BASE, "ACCESS_TOKEN": ""}.items():
            monkeypatch.setenv(k, v)
        result = scheduler.main()
        assert result["statusCode"] == 400
        assert "ACCESS_TOKEN" in result["body"]

    def test_missing_request_note_returns_400(self, monkeypatch):
        for k, v in {**ENV_BASE, "REQUEST_NOTE": ""}.items():
            monkeypatch.setenv(k, v)
        result = scheduler.main()
        assert result["statusCode"] == 400
        assert "REQUEST_NOTE" in result["body"]

    def test_zero_request_amount_returns_400(self, monkeypatch):
        for k, v in {**ENV_BASE, "REQUEST_AMOUNT": "0"}.items():
            monkeypatch.setenv(k, v)
        result = scheduler.main()
        assert result["statusCode"] == 400
        assert "REQUEST_AMOUNT" in result["body"]

    def test_empty_request_users_returns_400(self, monkeypatch):
        for k, v in {**ENV_BASE, "REQUEST_USERS": ""}.items():
            monkeypatch.setenv(k, v)
        result = scheduler.main()
        assert result["statusCode"] == 400
        assert "REQUEST_USERS" in result["body"]

    def test_whitespace_only_users_returns_400(self, monkeypatch):
        for k, v in {**ENV_BASE, "REQUEST_USERS": "  ,  "}.items():
            monkeypatch.setenv(k, v)
        result = scheduler.main()
        assert result["statusCode"] == 400


class TestPaymentFlow:
    @patch("venmo_scheduler.venmo_scheduler.Venmo")
    @patch("venmo_scheduler.venmo_scheduler.is_request_sent", return_value=False)
    def test_send_request_false_skips_payment(self, mock_is_sent, mock_venmo_cls, monkeypatch):
        for k, v in ENV_BASE.items():
            monkeypatch.setenv(k, v)
        mock_venmo_cls.return_value = make_venmo_mock()

        result = scheduler.main()

        mock_venmo_cls.return_value._send_request.assert_not_called()
        assert result["statusCode"] == 200

    @patch("venmo_scheduler.venmo_scheduler.Venmo")
    @patch("venmo_scheduler.venmo_scheduler.is_request_sent", return_value=False)
    def test_send_request_true_sends_payment(self, mock_is_sent, mock_venmo_cls, monkeypatch):
        for k, v in {**ENV_BASE, "SEND_REQUEST": "TRUE"}.items():
            monkeypatch.setenv(k, v)
        mock_venmo_cls.return_value = make_venmo_mock()

        result = scheduler.main()

        mock_venmo_cls.return_value._send_request.assert_called_once()
        assert result["statusCode"] == 200

    @patch("venmo_scheduler.venmo_scheduler.Venmo")
    @patch("venmo_scheduler.venmo_scheduler.is_request_sent", return_value=True)
    def test_already_sent_this_month_skips_payment(self, mock_is_sent, mock_venmo_cls, monkeypatch):
        for k, v in {**ENV_BASE, "SEND_REQUEST": "TRUE"}.items():
            monkeypatch.setenv(k, v)
        mock_venmo_cls.return_value = make_venmo_mock()

        result = scheduler.main()

        mock_venmo_cls.return_value._send_request.assert_not_called()
        assert result["statusCode"] == 200

    @patch("venmo_scheduler.venmo_scheduler.Venmo")
    def test_user_not_found_continues_without_crashing(self, mock_venmo_cls, monkeypatch):
        for k, v in {**ENV_BASE, "SEND_REQUEST": "TRUE"}.items():
            monkeypatch.setenv(k, v)
        mock_venmo = MagicMock()
        mock_venmo._validate_user.return_value = None
        mock_venmo._get_charge_payments.return_value = []
        mock_venmo_cls.return_value = mock_venmo

        result = scheduler.main()

        mock_venmo._send_request.assert_not_called()
        assert result["statusCode"] == 200

    @patch("venmo_scheduler.venmo_scheduler.Venmo")
    @patch("venmo_scheduler.venmo_scheduler.is_request_sent", return_value=False)
    def test_charge_payments_fetched_once_for_multiple_users(self, mock_is_sent, mock_venmo_cls, monkeypatch):
        for k, v in {**ENV_BASE, "REQUEST_USERS": "alice,bob,carol"}.items():
            monkeypatch.setenv(k, v)
        mock_venmo = make_venmo_mock()
        mock_venmo_cls.return_value = mock_venmo

        scheduler.main()

        mock_venmo._get_charge_payments.assert_called_once()

    @patch("venmo_scheduler.venmo_scheduler.Venmo")
    @patch("venmo_scheduler.venmo_scheduler.is_request_sent", return_value=False)
    def test_multiple_users_all_processed(self, mock_is_sent, mock_venmo_cls, monkeypatch):
        for k, v in {**ENV_BASE, "REQUEST_USERS": "alice,bob", "SEND_REQUEST": "TRUE"}.items():
            monkeypatch.setenv(k, v)
        mock_venmo = make_venmo_mock()
        mock_venmo_cls.return_value = mock_venmo

        scheduler.main()

        assert mock_venmo._validate_user.call_count == 2
        assert mock_venmo._send_request.call_count == 2


class TestRunLambda:
    def test_run_lambda_returns_main_result(self):
        with patch("venmo_scheduler.venmo_scheduler.main", return_value={"statusCode": 200, "body": "ok"}) as mock_main:
            result = scheduler.run_lambda({}, {})
            assert result == {"statusCode": 200, "body": "ok"}
