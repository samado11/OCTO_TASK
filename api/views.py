from datetime import datetime

from django.utils import dateparse, timezone
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, response, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Client, Loan,Account
from api.serializers import ClientSerializer, LoanSerializer, PaymentSerializer,AccountSerializer


class LoanViewSet(viewsets.ModelViewSet):

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @action(detail=True, methods=["post", "get"])
    def payments(self, request, pk=None):
        obj = self.get_object()
        if request.method == "GET":
            return response.Response(
                PaymentSerializer(obj.payment_set.all(), many=True).data,
                status=status.HTTP_200_OK,
            )
        payment = request.data
        payment["loan"] = pk
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def balance(self, request, pk=None):
        date = request.query_params.get("date", None)

        if not date:
            date = timezone.now()
        else:
            try:
                date = datetime.fromisoformat(date)
            except ValueError:
                date = dateparse.parse_datetime(date)

            if type(date) == datetime and not date.tzinfo:
                date = timezone.make_aware(date)

        loan = self.get_object()
        return response.Response({"Remaining": loan.balance(date)}, status=200)


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer

    def get_queryset(self):
        queryset = Client.objects.all()
        nid = self.request.query_params.get("nid", None)
        email = self.request.query_params.get("email", None)
        telephone = self.request.query_params.get("telephone", None)
        if nid:
            queryset = queryset.filter(nid=nid)
        if email:
            queryset = queryset.filter(email=email)
        if telephone:
            queryset = queryset.filter(telephone=telephone)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"client_id": serializer.data["id"]},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = Account.objects.all()
        balance = self.request.query_params.get("balance", None)
        pin = self.request.query_params.get("pin", None)
        user_id = self.request.query_params.get("user_id", None)
        if balance:
            queryset = queryset.filter(balance=balance)
        if pin:
            queryset = queryset.filter(pin=pin)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"account_id": serializer.data["id"]},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

schema_view = get_schema_view(
    openapi.Info(
        title="LoanSystem",
        default_version="v1",
        description="Octo Task"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    validators=["ssv"],
)
