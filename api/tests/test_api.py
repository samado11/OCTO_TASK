from datetime import timedelta
from decimal import Decimal
from urllib import parse

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from api.tests.utils import create_client,create_account


class TestLoan(TestCase):
    def setUp(self) -> None:
        self.api = APIClient()
        self.loan_id = None
        self.payment_id = None

    def _new_loan(self) -> int:
        if self.loan_id:
            return 201
        account_id = create_account().data.get("account_id")
        post = {
            "amount": 1000,
            "rate": 0.05,
            "date": timezone.now(),
            "account": account_id,
        }
        resp = self.api.post("/api/loans/", post, format="json")
        if resp.status_code == 201:
            self.loan_id = resp.data.get("loan_id", None)
        return resp.status_code

    def _new_payment(self) -> int:
        self._new_loan()

        if self.payment_id:
            return 201

        post = {"payment": "made", "date": timezone.now(), "amount": 560}
        resp = self.api.post(
            f"/api/loans/{self.loan_id}/payments/", post, format="json"
        )

        if resp.status_code == 201:
            self.payment_id = resp.data.get("amount", None)

        return resp.status_code

    def test_new_loan(self) -> None:
        status = self._new_loan()
        self.assertEqual(status, 201)


    def test_new_payment(self) -> None:
        status = self._new_payment()
        self.assertEqual(status, 201)

    def test_loan_balance(self) -> None:
        self._new_payment()
        date = parse.quote_plus(str(timezone.now()))
        resp = self.api.get(
            f"/api/loans/{self.loan_id}/balance/?date={date}", format="json"
        )
       
        self.assertEqual(resp.status_code, 200)

    def test_loan_balance_value(self) -> None:
        self._new_payment()
        date = parse.quote_plus(str(timezone.now()))
        resp = self.api.get(
            f"/api/loans/{self.loan_id}/balance/?date={date}", format="json"
        )
        balance = resp.data.get("Remaining")
        self.assertEqual(balance, Decimal("477.654320987654320987654321"))

    def test_loan_balance_incorrect_value(self) -> None:
        self._new_payment()
        date = parse.quote_plus(str(timezone.now() - timedelta(hours=1)))
        resp = self.api.get(
            f"/api/loans/{self.loan_id}/balance/?date={date}", format="json"
        )
        balance = resp.data.get("Remaining")
        self.assertEqual(balance, Decimal("1037.654320987654320987654321"))


class TestClient(TestCase):
    def test_post_client(self) -> None:
        res = create_client()
        self.assertEqual(201, res.status_code)
        self.assertEqual({"client_id"}, res.data.keys())
