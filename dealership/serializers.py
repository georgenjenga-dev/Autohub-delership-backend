from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Brand,
    Vehicle,
    VehicleImage,
    Reservation,
    Inquiry,
    Payment,
    KanbanTask,
)

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

class VehicleSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Vehicle
        fields = "__all__"

class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = "__all__"

class ReservationSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.CharField(
        source="vehicle.model",
        read_only=True
    )

    brand = serializers.CharField(
        source="vehicle.brand.name",
        read_only=True
    )

    customer = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Reservation
        fields = "__all__"

class InquirySerializer(serializers.ModelSerializer):

    customer = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Inquiry
        fields = "__all__"

class PaymentSerializer(serializers.ModelSerializer):
    reservation_vehicle = serializers.CharField(
        source="reservation.vehicle.model",
        read_only=True
    )

    customer = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Payment
        fields = "__all__"

class KanbanTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanbanTask
        fields = "__all__"

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user        