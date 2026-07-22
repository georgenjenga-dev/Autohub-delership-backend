from django.contrib import admin
from .models import (
    Brand,
    Vehicle,
    VehicleImage,
    Reservation,
    Inquiry,
    Payment,
    KanbanTask,
)
admin.site.register(Brand)
admin.site.register(Vehicle)
admin.site.register(VehicleImage)
admin.site.register(Reservation)
admin.site.register(Inquiry)
admin.site.register(Payment)
admin.site.register(KanbanTask)