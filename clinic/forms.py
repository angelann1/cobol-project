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
    student = forms.ModelChoiceField(
        queryset=Student.objects.all().order_by('last_name', 'first_name'),
        empty_label="Select Student",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'width:100%; height:45px; font-size:14px;'
        })
    )

    class Meta:
        model = MedicalRecord
        fields = [
            'student', 'weight_kg', 'height_cm', 'blood_pressure', 'temperature',
            'chief_complaint', 'diagnosis', 'treatment_given',
            'medicines_dispensed', 'referred_to_hospital', 'notes'
        ]
        widgets = {
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:100%; height:45px;'}),
            'height_cm': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:100%; height:45px;'}),
            'blood_pressure': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:100%; height:45px;'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:100%; height:45px;'}),
            'chief_complaint': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:100%; height:45px;'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'treatment_given': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medicines_dispensed': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'referred_to_hospital': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'transform: scale(1.3); margin-left:10px;'})
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



