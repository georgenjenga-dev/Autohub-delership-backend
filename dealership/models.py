from django.db import models
from django.contrib.auth.models import User

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    FUEL_CHOICES = [
        ("Petrol", "Petrol"),
        ("Diesel", "Diesel"),
        ("Electric", "Electric"),
        ("Hybrid", "Hybrid"),
    ]

    TRANSMISSION_CHOICES = [
        ("Automatic", "Automatic"),
        ("Manual", "Manual"),
    ]

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="vehicles"
    )

    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.PositiveIntegerField()

    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES
    )

    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES
    )

    color = models.CharField(max_length=50)
    description = models.TextField()

    main_image = models.ImageField(
        upload_to="vehicles/",
        blank=True,
        null=True
    )

    

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand.name} {self.model}"

class VehicleImage(models.Model):
     vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="images"
    )

     image = models.ImageField(
        upload_to="vehicle_images/"
    )

     caption = models.CharField(
        max_length=100,
        blank=True
    )

     uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

     def __str__(self):
        return f"{self.vehicle.model} Image"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Declined", "Declined"),
        ("Completed", "Completed"),
    ]

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    reservation_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.customer.username} - {self.vehicle.model}"


class Inquiry(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="inquiries"
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="inquiries"
    )

    message = models.TextField()

    inquiry_date = models.DateTimeField(auto_now_add=True)

    is_responded = models.BooleanField(default=False)

    def __str__(self):
        return f"Inquiry by {self.customer.username} about {self.vehicle.model}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("Bank Transfer", "Bank Transfer"),
        ("M-Pesa", "M-Pesa"),
        ("Cash", "Cash"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
    ]

    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    bank_name = models.CharField(
        max_length=100,
        blank=True
    )

    account_number = models.CharField(
        max_length=50,
        blank=True
    )

    transaction_reference = models.CharField(
        max_length=100,
        unique=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.amount}"


class KanbanTask(models.Model):
    STATUS_CHOICES = [
        ("To Do", "To Do"),
        ("In Progress", "In Progress"),
        ("Done", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="To Do"
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )

    due_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title