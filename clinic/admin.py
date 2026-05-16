from django.contrib import admin
from .models import Student, MedicalRecord, Medicine, StockMovement, Appointment

admin.site.register(Student)
admin.site.register(MedicalRecord)
admin.site.register(StockMovement)
admin.site.register(Appointment)