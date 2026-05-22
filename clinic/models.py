from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django import forms

class Student(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    YEAR_LEVEL_CHOICES = [
        ('Grade 7', 'Grade 7'), ('Grade 8', 'Grade 8'),
        ('Grade 9', 'Grade 9'), ('Grade 10', 'Grade 10'),
        ('Grade 11', 'Grade 11'), ('Grade 12', 'Grade 12'),
        ('1st Year', '1st Year'), ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'), ('4th Year', '4th Year'),
    ]

    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    year_level = models.CharField(max_length=20, choices=YEAR_LEVEL_CHOICES)
    section = models.CharField(max_length=50, blank=True)
    course_or_strand = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    contact_number = models.CharField(max_length=11, blank=False, validators=[RegexValidator(regex=r'^\d{11}$')])
    guardian_name = models.CharField(max_length=200, blank=True)
    guardian_contact = models.CharField(max_length=11, blank=False, validators=[RegexValidator(regex=r'^\d{11}$')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.student_id})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class MedicalRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='medical_records')
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    blood_pressure = models.CharField(max_length=20, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    chief_complaint = models.CharField(max_length=200)
    diagnosis = models.TextField()
    treatment_given = models.TextField()
    medicines_dispensed = models.TextField(blank=True)
    referred_to_hospital = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} — {self.date}"


class Medicine(models.Model):
    UNIT_CHOICES = [
        ('tablets', 'Tablets'),
        ('capsules', 'Capsules'),
        ('bottles', 'Bottles'),
        ('sachets', 'Sachets'),
        ('ampules', 'Ampules'),
        ('pieces', 'Pieces'),
    ]

    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=10)
    expiry_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold

    def __str__(self):
        return f"{self.name} ({self.generic_name})" if self.generic_name else self.name


class StockMovement(models.Model):
    MOVEMENT_TYPES = [('IN', 'Stock In'), ('OUT', 'Dispensed to Student')]

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='movements')
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='medicines_received')
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.medicine} — {self.movement_type} — {self.quantity}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('No Show', 'No Show'),
    ]
    PURPOSE_CHOICES = [
        ('General Checkup', 'General Checkup'),
        ('Follow-up', 'Follow-up'),
        ('Medical Certificate', 'Medical Certificate'),
        ('Emergency', 'Emergency'),
        ('Vaccination', 'Vaccination'),
        ('Others', 'Others'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    purpose = models.CharField(max_length=100, choices=PURPOSE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.student} — {self.date} {self.time}"