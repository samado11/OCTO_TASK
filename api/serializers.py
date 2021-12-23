from rest_framework import serializers
from decimal import Decimal

from api.models import Client, Loan, Payment,Account


class LoanSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(required=False, format="hex")
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    rate = serializers.DecimalField(max_digits=20, decimal_places=2)
    date = serializers.DateTimeField()
    installment = serializers.SerializerMethodField()
    loan_id = serializers.SerializerMethodField()
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=True, write_only=True)

    def get_installment(self, loan: Loan) -> Decimal:
        return loan.installment

    def get_loan_id(self, loan: Loan) -> str:
        return str(loan.id)

    class Meta:
        model = Loan
        exclude = ("updated", "active")


class PaymentSerializer(serializers.ModelSerializer):
    def validate(self, data: dict) -> dict:
        payment = Payment(**data)

        try:
            payment.validate()


        except ValueError as e:
            raise serializers.ValidationError({"error": e})

        return data

    class Meta:
        model = Payment
        exclude = ("updated", "active")


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ("updated", "active")

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ("updated", "active")