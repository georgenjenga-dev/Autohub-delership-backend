from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    RegisterSerializer,
    BrandSerializer,
    VehicleSerializer,
    VehicleImageSerializer,
    ReservationSerializer,
    InquirySerializer,
    PaymentSerializer,
    KanbanTaskSerializer,
)

from .models import (
    Brand,
    Vehicle,
    VehicleImage,
    Reservation,
    Inquiry,
    Payment,
    KanbanTask,
)


# ===========================
# CURRENT USER
# ===========================

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "is_staff": request.user.is_staff,
            "is_superuser": request.user.is_superuser,
        })


# ===========================
# DASHBOARD STATS
# ===========================

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


# ===========================
# BRANDS
# ===========================

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


# ===========================
# VEHICLES
# ===========================

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


# ===========================
# VEHICLE IMAGES
# ===========================

class VehicleImageViewSet(viewsets.ModelViewSet):
    queryset = VehicleImage.objects.all()
    serializer_class = VehicleImageSerializer


# ===========================
# RESERVATIONS
# ===========================

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=False, methods=["get"])
    def my_reservations(self, request):
        reservations = Reservation.objects.filter(customer=request.user)
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)


# ===========================
# INQUIRIES
# ===========================

class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def my_inquiries(self, request):
        inquiries = Inquiry.objects.filter(customer=request.user)
        serializer = self.get_serializer(inquiries, many=True)
        return Response(serializer.data)


# ===========================
# PAYMENTS
# ===========================

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=False, methods=["get"])
    def my_payments(self, request):
        payments = Payment.objects.filter(customer=request.user)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)


# ===========================
# KANBAN
# ===========================

class KanbanTaskViewSet(viewsets.ModelViewSet):
    queryset = KanbanTask.objects.all()
    serializer_class = KanbanTaskSerializer


# ===========================
# REGISTER
# ===========================

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer