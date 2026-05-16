from django import forms
from .models import Student, MedicalRecord, Medicine, StockMovement, Appointment

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'date_of_birth',
                  'gender', 'year_level', 'section', 'course_or_strand',
                  'address', 'contact_number', 'guardian_name', 'guardian_contact']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['weight_kg', 'height_cm', 'blood_pressure', 'temperature',
                  'chief_complaint', 'diagnosis', 'treatment_given',
                  'medicines_dispensed', 'referred_to_hospital', 'notes']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'treatment_given': forms.Textarea(attrs={'rows': 3}),
            'medicines_dispensed': forms.Textarea(attrs={'rows': 2}),
        }

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'generic_name', 'unit', 'quantity',
                  'low_stock_threshold', 'expiry_date', 'description']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['movement_type', 'quantity', 'notes']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['student', 'date', 'time', 'purpose', 'status', 'assigned_to', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }