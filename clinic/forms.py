from django import forms
from .models import Student, MedicalRecord, Appointment, Medicine, MedicalRecord

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
        # Added 'student' as the very first field so your HTML template tag renders successfully
        fields = [
            'student', 'weight_kg', 'height_cm', 'blood_pressure', 'temperature',
            'chief_complaint', 'diagnosis', 'treatment_given',
            'medicines_dispensed', 'referred_to_hospital', 'notes'
        ]
        widgets = {
            'chief_complaint': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What are the current symptoms...'}),
            'diagnosis': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Clinical impression or assessment...'}),
            'treatment_given': forms.Textarea(attrs={'rows': 3, 'placeholder': 'First aid or treatment administered...'}),
            'medicines_dispensed': forms.Textarea(attrs={'rows': 2, 'placeholder': 'e.g., Paracetamol 500mg x1...'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Additional health progression notes...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Automatically links up form fields with your frontend layout classes
        for field_name, field in self.fields.items():
            # Apply class to everything EXCEPT checkboxes
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control-rec'})


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['student', 'date', 'time', 'purpose', 'status', 'assigned_to', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'generic_name', 'unit', 'quantity', 'low_stock_threshold', 'expiry_date', 'description']
        widgets = {
            'name':               forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Paracetamol'}),
            'generic_name':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Acetaminophen'}),
            'unit':               forms.Select(attrs={'class': 'form-control'}),
            'quantity':           forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'low_stock_threshold':forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'expiry_date':        forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description':        forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'unit' in self.fields:
            # 1. Handle ForeignKey relations
            self.fields['unit'].empty_label = "Select Unit"
            
            # 2. Handle CharField choice lists (removes Django's fallback dashes option)
            if hasattr(self.fields['unit'], 'choices'):
                cleaned_choices = [choice for choice in self.fields['unit'].choices if choice[0] != '']
                # Insert a clean placeholder text structure at the start instead
                self.fields['unit'].choices = [('', 'Select Unit')] + cleaned_choices


# class MedicalRecordForm(forms.ModelForm):
#     class Meta:
#         model = MedicalRecord
#         # Update this list to match ONLY the field names that exist inside your models.py file
#         fields = ['student', 'complaint', 'diagnosis', 'treatment']
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Apply the layout CSS classes to match the look of your UI dashboard modal
#         for field_name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'form-control-rec'})