from django.contrib import admin
from .models import Student, MedicalRecord, Appointment

admin.site.register(Student)
admin.site.register(MedicalRecord)
admin.site.register(Appointment)