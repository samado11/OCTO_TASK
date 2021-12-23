import uuid
from decimal import ROUND_HALF_UP, Decimal

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField()
    updated = models.DateTimeField( auto_now_add=True)
    active = models.BooleanField( default=True)

    class Meta:
        abstract = True

class Client(Base):

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    telephone = models.CharField(max_length=20, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    nid = models.CharField(max_length=14, unique=True)

    def __str__(self) -> str:
        return str(self.name)

class Account(Base):
    balance = models.IntegerField()
    pin = models.CharField(max_length=6)
    user_id = models.ForeignKey(Client , on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.user_id)

class Loan(Base):
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    rate = models.DecimalField(max_digits=20, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    def balance(self, date: timezone.datetime = timezone.now()) -> Decimal:
        payments = self.payment_set.filter(payment=Payment.MADE)
        payments = payments.filter(date__lte=date) if date else payments
        debit = self.installment * 2
        credit = sum(payments.values_list("amount", flat=True))
        return Decimal(debit - credit)

    @property
    def installment(self) -> Decimal:
        rate = Decimal(f"{self.rate}")
        term = 2
        r = rate / term
        exact_installment = (r + r / ((1 + r) ** term - 1)) * self.amount
        return exact_installment

    def __str__(self) -> str:
        return f"{self.id}"


class Payment(Base):

    MADE = "made"
    MISSED = "missed"
    PAYMENTS = ((MADE, "made"), (MISSED, "missed"))
    loan = models.ForeignKey(to="api.Loan", on_delete=models.CASCADE)
    payment = models.CharField(max_length=6, choices=PAYMENTS, default=MISSED)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    def validate(self) -> None:
        if self.amount < self.loan.installment:
            raise ValueError(f"You must pay ${self.loan.installment}")
        
        if self.amount > self.loan.account.balance:
            raise ValueError(f"No enough credit")
        b=self.loan.account.balance
        a=self.amount
        Account.objects.filter(id=self.loan.account.id).update(balance=b - a)


    def __str__(self) -> str:
        return str(self.id)


