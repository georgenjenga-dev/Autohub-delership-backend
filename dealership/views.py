from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .permissions import IsAdminOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

from .serializers import RegisterSerializer

from .models import (
    Brand,
    Vehicle,
    VehicleImage,
    Reservation,
    Inquiry,
    Payment,
    KanbanTask,
)

from .serializers import (
    BrandSerializer,
    VehicleSerializer,
    VehicleImageSerializer,
    ReservationSerializer,
    InquirySerializer,
    PaymentSerializer,
    KanbanTaskSerializer,
)

class DashboardStats(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = {
            "vehicles": Vehicle.objects.count(),
            "available_vehicles": Vehicle.objects.filter(is_available=True).count(),
            "brands": Brand.objects.count(),
            "reservations": Reservation.objects.count(),
            "payments": Payment.objects.count(),
            "customers": User.objects.count(),
        }

        return Response(data)


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "brand",
        "fuel_type",
        "transmission",
        "year",
        "is_available",
    ]

    search_fields = [
        "model",
        "brand__name",
        "description",
    ]

    ordering_fields = [
        "price",
        "year",
        "created_at",
    ]

class VehicleImageViewSet(viewsets.ModelViewSet):
    queryset = VehicleImage.objects.all()
    serializer_class = VehicleImageSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def my_reservations(self, request):
        reservations = Reservation.objects.filter(customer=request.user)
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def my_inquiries(self, request):
        inquiries = Inquiry.objects.filter(customer=request.user)
        serializer = self.get_serializer(inquiries, many=True)
        return Response(serializer.data)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def my_payments(self, request):
        payments = Payment.objects.filter(customer=request.user)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)



class KanbanTaskViewSet(viewsets.ModelViewSet):
    queryset = KanbanTask.objects.all()
    serializer_class = KanbanTaskSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer