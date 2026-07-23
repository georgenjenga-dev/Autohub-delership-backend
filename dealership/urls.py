from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    DashboardStats,
    CurrentUserView,
    BrandViewSet,
    VehicleViewSet,
    VehicleImageViewSet,
    ReservationViewSet,
    InquiryViewSet,
    PaymentViewSet,
    KanbanTaskViewSet,
)


router = DefaultRouter()

router.register(r'brands', BrandViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'vehicle-images', VehicleImageViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'inquiries', InquiryViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'kanban', KanbanTaskViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
    path("dashboard/", DashboardStats.as_view(), name="dashboard"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
]