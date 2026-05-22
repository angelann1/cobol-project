from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, MedicalRecord, Appointment, Medicine, StockMovement
from .forms import StudentForm, MedicalRecordForm, AppointmentForm, MedicineForm
from .models import MedicalRecord, Student
from django.utils import timezone



# ── DASHBOARD ──────────────────────────────
@login_required
def dashboard(request):
    total_students = Student.objects.count()
    scheduled_count = Appointment.objects.filter(status='Scheduled').count()
    completed_count = Appointment.objects.filter(status='Completed').count()
    cancelled_count = Appointment.objects.filter(status='Cancelled').count()
    total_appointments = Appointment.objects.count()
    upcoming_appointments = Appointment.objects.filter(status='Scheduled').order_by('date', 'time')[:5]
    recent_records = MedicalRecord.objects.all().order_by('-date')[:5]


    context = {
        'total_students': total_students,
        'upcoming_appointments': upcoming_appointments,
        'recent_records': recent_records,
        'scheduled_count': scheduled_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'total_appointments': total_appointments,
        'total_medicines': Medicine.objects.count(),
        'low_stock_count': Medicine.objects.filter(quantity__lte=10).count(),
    }
    return render(request, 'clinic/dashboard.html', context)


# ── STUDENTS ───────────────────────────────
@login_required
def student_list(request):
    query = request.GET.get('q', '')
    students = Student.objects.filter(
        last_name__icontains=query) if query else Student.objects.all().order_by('last_name')
    return render(request, 'clinic/student_list.html', {'students': students, 'query': query})


@login_required
def student_add(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student added successfully.')
        return redirect('student_list')
    return render(request, 'clinic/form.html', {'form': form, 'title': 'Add Student'})


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    records = student.medical_records.order_by('-date')
    appointments = student.appointments.order_by('-date')
    return render(request, 'clinic/student_detail.html', {
        'student': student, 'records': records, 'appointments': appointments
    })


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.student_id = request.POST.get('student_id')
        full_name = request.POST.get('full_name', '').strip()
        name_parts = full_name.split(' ', 1)
        student.first_name = name_parts[0]
        student.last_name = name_parts[1] if len(name_parts) > 1 else ''
        student.gender = request.POST.get('gender')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.year_level = request.POST.get('year_level')
        student.section = request.POST.get('section')
        student.course_or_strand = request.POST.get('course_or_strand')
        student.contact_number = request.POST.get('contact_number')
        student.guardian_name = request.POST.get('guardian_name')
        student.guardian_contact = request.POST.get('guardian_contact')
        student.address = request.POST.get('address')
        student.save()
        messages.success(request, 'Student updated successfully.')
        return redirect('student_list')
    return render(request, 'clinic/editstudent.html', {'student': student})


# ── MEDICAL RECORDS ────────────────────────
@login_required
def record_add(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    form = MedicalRecordForm(request.POST or None)
    if form.is_valid():
        record = form.save(commit=False)
        record.student = student
        record.recorded_by = request.user
        record.save()
        messages.success(request, 'Medical record saved.')
        return redirect('student_detail', pk=student_pk)
    return render(request, 'clinic/form.html', {'form': form, 'title': f'New Record — {student}'})


# ── APPOINTMENTS ───────────────────────────
@login_required
def appointment_list(request):
    appointments = Appointment.objects.all().order_by('date', 'time')
    return render(request, 'clinic/appointment_list.html', {'appointments': appointments})


@login_required
def appointment_add(request):
    form = AppointmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Appointment scheduled.')
        return redirect('appointment_list')
    return render(request, 'clinic/form.html', {'form': form, 'title': 'Schedule Appointment'})


@login_required
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    form = AppointmentForm(request.POST or None, instance=appointment)
    if form.is_valid():
        form.save()
        messages.success(request, 'Appointment updated.')
        return redirect('appointment_list')
    return render(request, 'clinic/form.html', {'form': form, 'title': 'Edit Appointment'})


@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted.')
    return redirect('appointment_list')


# ── MEDICINES ───────────────────────────────
@login_required
def medicine_list(request):
    medicines = Medicine.objects.all().order_by('name')
    low_stock = medicines.filter(quantity__lte=10)
    return render(request, 'clinic/medicine_list.html', {
        'medicines': medicines,
        'low_stock_count': low_stock.count(),
        'total_count': medicines.count(),
    })


@login_required
def medicine_add(request):
    form = MedicineForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Medicine added to inventory.')
        return redirect('medicine_list')
    return render(request, 'clinic/medicine_form.html', {'form': form, 'title': 'Add Medicine', 'action': 'Add'})


@login_required
def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    form = MedicineForm(request.POST or None, instance=medicine)
    if form.is_valid():
        form.save()
        messages.success(request, 'Medicine updated.')
        return redirect('medicine_list')
    return render(request, 'clinic/medicine_form.html', {'form': form, 'title': 'Edit Medicine', 'action': 'Update', 'medicine': medicine})


@login_required
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.delete()
        messages.success(request, 'Medicine deleted.')
    return redirect('medicine_list')


@login_required
def medicine_restock(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 0))
        if qty > 0:
            medicine.quantity += qty
            medicine.save()
            StockMovement.objects.create(
                medicine=medicine,
                movement_type='IN',
                quantity=qty,
                performed_by=request.user,
                notes=request.POST.get('notes', '')
            )
            messages.success(request, f'Restocked {qty} units of {medicine.name}.')
    return redirect('medicine_list')

from django.utils import timezone

@login_required
def medical_record_list(request):
    records = MedicalRecord.objects.all().order_by('-date')
    today = timezone.now().date()
    context = {
        'records': records,
        'total_records': records.count(),
        'unique_students': records.values('student').distinct().count(),
        'referred_count': records.filter(referred_to_hospital=True).count(),
        'today_count': records.filter(date=today).count(),
    }
    return render(request, 'clinic/medical_record_list.html', context)


@login_required
def medical_records(request):
    """
    Display all medical records with summary statistics.
    Context expected by medical_records.html:
      - records         → queryset of all MedicalRecord objects
      - students        → queryset of all Student objects (for the Add form dropdown)
      - total_records   → int
      - unique_students → int
      - referred_count  → int
      - today_count     → int
    """
    today = timezone.localdate()
 
    all_records = (
        MedicalRecord.objects
        .select_related('student', 'recorded_by')
        .order_by('-date', '-id')
    )
 
    context = {
        'records':         all_records,
        'students':        Student.objects.order_by('last_name', 'first_name'),
        'total_records':   all_records.count(),
        'unique_students': all_records.values('student').distinct().count(),
        'referred_count':  all_records.filter(referred_to_hospital=True).count(),
        'today_count':     all_records.filter(date=today).count(),
    }
    return render(request, 'clinic/medical_records.html', context)
 
 
# ─────────────────────────────────────────────────────────────
#  Add Medical Record
# ─────────────────────────────────────────────────────────────
# @login_required
# def add_medical_record(request):
#     """
#     Handle POST from the Add Record modal form.
#     On success  → redirect back to medical_records with a success message.
#     On GET      → redirect to medical_records (modal lives on that page).
#     """
#     if request.method != 'POST':
#         return redirect('medical_records')
 
#     post = request.POST
 
#     # ── Required fields ──────────────────────────────────────
#     student_id     = post.get('student', '').strip()
#     date_str       = post.get('date', '').strip()
#     chief_complaint = post.get('chief_complaint', '').strip()
 
#     if not student_id or not date_str or not chief_complaint:
#         messages.error(request, 'Please fill in all required fields.')
#         return redirect('medical_records')
 
#     try:
#         student = Student.objects.get(pk=student_id)
#     except Student.DoesNotExist:
#         messages.error(request, 'Selected student not found.')
#         return redirect('medical_records')
 
#     # ── Optional fields ───────────────────────────────────────
#     diagnosis           = post.get('diagnosis', '').strip()
#     treatment_given     = post.get('treatment_given', '').strip()
#     medicines_dispensed = post.get('medicines_dispensed', '').strip()
#     notes               = post.get('notes', '').strip()
#     blood_pressure      = post.get('blood_pressure', '').strip()
 
#     # Numeric vitals – ignore empty / invalid values
#     weight_kg   = _parse_decimal(post.get('weight_kg'))
#     height_cm   = _parse_decimal(post.get('height_cm'))
#     temperature = _parse_decimal(post.get('temperature'))
 
#     # Referred toggle comes in as the string 'true' or 'false'
#     referred_to_hospital = post.get('referred_to_hospital', 'false').lower() == 'true'
 
#     # ── Create record ─────────────────────────────────────────
#     MedicalRecord.objects.create(
#         student              = student,
#         date                 = date_str,
#         chief_complaint      = chief_complaint,
#         diagnosis            = diagnosis,
#         treatment_given      = treatment_given,
#         medicines_dispensed  = medicines_dispensed,
#         notes                = notes,
#         weight_kg            = weight_kg,
#         height_cm            = height_cm,
#         blood_pressure       = blood_pressure,
#         temperature          = temperature,
#         referred_to_hospital = referred_to_hospital,
#         recorded_by          = request.user,
#     )
 
#     messages.success(
#         request,
#         f'Medical record for {student.get_full_name()} saved successfully!'
#     )
#     return redirect('medical_records')
 
 
# # ─────────────────────────────────────────────────────────────
# #  Helper
# # ─────────────────────────────────────────────────────────────
# def _parse_decimal(value):
#     """Return a float from a string, or None if empty / invalid."""
#     if not value or str(value).strip() == '':
#         return None
#     try:
#         return float(value)
#     except (ValueError, TypeError):
#         return None
 

@login_required
def medical_records(request):
    today = timezone.localdate()
 
    all_records = (
        MedicalRecord.objects
        .select_related('student', 'recorded_by')
        .order_by('-date', '-id')
    )
 
    context = {
        'records':         all_records,
        # ← This is what populates the student picker dropdown
        'students':        Student.objects.all().order_by('last_name', 'first_name'),
        'total_records':   all_records.count(),
        'unique_students': all_records.values('student').distinct().count(),
        'referred_count':  all_records.filter(referred_to_hospital=True).count(),
        'today_count':     all_records.filter(date=today).count(),
    }
    return render(request, 'clinic/medical_records.html', context)
 
 
# ─────────────────────────────────────────────────────────────
#  Add Medical Record
# ─────────────────────────────────────────────────────────────
@login_required
def add_medical_record(request):
    if request.method != 'POST':
        return redirect('medical_records')
 
    post = request.POST
 
    # ── Required fields ──────────────────────────────────────
    student_pk      = post.get('student', '').strip()
    chief_complaint = post.get('chief_complaint', '').strip()
 
    if not student_pk or not chief_complaint:
        messages.error(request, 'Please fill in all required fields.')
        return redirect('medical_records')
 
    try:
        student = Student.objects.get(pk=student_pk)
    except Student.DoesNotExist:
        messages.error(request, 'Selected student not found.')
        return redirect('medical_records')
 
    # ── Optional text fields (default '' so TextField is never None) ──
    diagnosis           = post.get('diagnosis', '').strip()
    treatment_given     = post.get('treatment_given', '').strip()
    medicines_dispensed = post.get('medicines_dispensed', '').strip()
    notes               = post.get('notes', '').strip()
    blood_pressure      = post.get('blood_pressure', '').strip()
 
    # ── Numeric vitals ────────────────────────────────────────
    weight_kg   = _parse_decimal(post.get('weight_kg'))
    height_cm   = _parse_decimal(post.get('height_cm'))
    temperature = _parse_decimal(post.get('temperature'))
 
    # ── Referred toggle ('true' / 'false' string from JS) ─────
    referred_to_hospital = post.get('referred_to_hospital', 'false').lower() == 'true'
 
    # ── Create record ─────────────────────────────────────────
    # NOTE: `date` is NOT passed because the model uses auto_now_add=True
    #       which sets it to today automatically.
    MedicalRecord.objects.create(
        student              = student,
        chief_complaint      = chief_complaint,
        diagnosis            = diagnosis,
        treatment_given      = treatment_given,
        medicines_dispensed  = medicines_dispensed,
        notes                = notes,
        weight_kg            = weight_kg,
        height_cm            = height_cm,
        blood_pressure       = blood_pressure,
        temperature          = temperature,
        referred_to_hospital = referred_to_hospital,
        recorded_by          = request.user,
    )
 
    messages.success(
        request,
        f'Medical record for {student.get_full_name()} saved successfully!'
    )
    return redirect('medical_records')
 
 
# ─────────────────────────────────────────────────────────────
#  Helper
# ─────────────────────────────────────────────────────────────
def _parse_decimal(value):
    """Return a float from a string, or None if empty / invalid."""
    if not value or str(value).strip() == '':
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None
    

