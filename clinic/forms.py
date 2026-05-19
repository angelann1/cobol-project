from django import forms
from .models import Student, MedicalRecord, Appointment

COURSE_CHOICES = [
    ('', 'Select Course or Strand'),
    ('Senior High School', (
        ('STEM', 'STEM — Science, Technology, Engineering & Math'),
        ('HUMSS', 'HUMSS — Humanities & Social Sciences'),
        ('ABM', 'ABM — Accountancy, Business & Management'),
        ('ICT', 'ICT — Information & Communications Technology'),
        ('TVL', 'TVL — Technical-Vocational-Livelihood'),
        ('GAS', 'GAS — General Academic Strand'),
    )),
    ('College', (
        ('CN', 'CN — College of Nursing'),
        ('CHTM', 'CHTM — College of Hospitality & Tourism Management'),
        ('ECE', 'ECE — Electronics & Communications Engineering'),
        ('CCS', 'CCS — College of Computer Studies'),
        ('CBA', 'CBA — College of Business Administration'),
        ('CAS', 'CAS — College of Arts & Sciences'),
        ('COE', 'COE — College of Engineering'),
    )),
]

class StudentForm(forms.ModelForm):
    course_or_strand = forms.ChoiceField(
        choices=COURSE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

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


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['student', 'date', 'time', 'purpose', 'status', 'assigned_to', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }