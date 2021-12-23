from django.core.handlers.wsgi import WSGIRequest
from datetime import datetime
from api.models import Payment, Loan, Client, Account
from rest_framework.test import APIClient
from typing import Union, Iterator, Type
from collections import namedtuple
from decimal import Decimal


def create_client_from_model(
    name: str = "mohamed",
    surname: str = "salah",
    email: str = "mohamed.salah@gov.uk",
    telephone: str = "01234567898",
    nid: str = "572597395058519",
    date: Union[datetime, str] = "2019-05-09 03:18Z",
) -> Client:
    client = Client.objects.create(
        name=name, surname=surname, email=email, telephone=telephone, nid=nid, date=date
    )

    return client

def create_account_from_model(
    user_id: Client ,
    balance: Decimal =10000.00,
    pin: Decimal =1919,
    date: Union[datetime, str] = "2019-05-09 03:18Z",
) -> Account:
    account = Account.objects.create(balance=balance, pin=pin, user_id=user_id,date=date)

    return account

def create_loan_from_model(
    account: Account,
    amount: Decimal = 15000,
    rate: Decimal = 0.10,
    date: Union[datetime, str] = "2019-05-09 03:18Z",
) -> Loan:
    return Loan.objects.create(amount=amount, rate=rate, date=date, account=account)


def create_payment_from_model(
    loan: Loan,
    payment: str = "made",
    date: Union[datetime, str] = "2019-06-09 03:18Z",
    amount: Decimal = 200.00,
) -> Payment:
    return Payment.objects.create(loan=loan, payment=payment, date=date, amount=amount)


def create_client() -> WSGIRequest:
    client_payload = {
        "name": "ahmed",
        "surname": "ahmar",
        "email": "ahmed@gmail.com",
        "telephone": "11984345678",
        "nid": "545687549",
        
    }
    api = APIClient()
    return api.post("/api/clients/", client_payload, format="json")

def create_account() -> WSGIRequest:
    u=create_client()
    account_payload = {
    "balance": 10000,
    "pin": 1919,
    "user_id": u.data.get("client_id"),
    "date": "2019-05-09 03:18Z"
}
    api = APIClient()
    return api.post("/api/accounts/", account_payload, format="json")

def __loans_named_tuple(loans_attr: list) -> Type[tuple]:
    return namedtuple("Loans", " ".join(loans_attr))

