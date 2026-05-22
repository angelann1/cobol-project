from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Student, MedicalRecord, Appointment, Medicine, StockMovement
from .forms import StudentForm, MedicalRecordForm, AppointmentForm, MedicineForm


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
    students = Student.objects.filter(last_name__icontains=query) if query else Student.objects.all().order_by('last_name')
    return render(request, 'clinic/student_list.html', {'students': students, 'query': query})


@login_required
def student_add(request):
    form = StudentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
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
def medical_record_list(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            if request.user.is_authenticated:
                record.recorded_by = request.user
            record.save()
            messages.success(request, "Medical record added successfully!")
            return redirect('medical_record_list')
        else:
            messages.error(request, "Failed to add record. Please resolve form evaluation errors.")
    else:
        form = MedicalRecordForm()

    all_records = MedicalRecord.objects.select_related('student', 'recorded_by').all().order_by('-date', '-id')
    today = timezone.localdate()

    context = {
        'records': all_records,
        'form': form,
        'total_records': all_records.count(),
        'unique_students': all_records.values('student').distinct().count(),
        'referred_count': all_records.filter(referred_to_hospital=True).count(),
        'today_count': all_records.filter(date=today).count(),
    }
    return render(request, 'clinic/medical_record_list.html', context)


@login_required
def record_add(request, student_pk):
    """
    Handles logging encounters directly linked from an explicit Student profile context.
    """
    student = get_object_or_404(Student, pk=student_pk)
    
    if request.method == 'POST':
        # Create a mutable copy of POST data to inject the target student id safely
        data = request.POST.copy()
        data['student'] = str(student.pk)
        form = MedicalRecordForm(data)
        
        if form.is_valid():
            record = form.save(commit=False)
            record.student = student
            if request.user.is_authenticated:
                record.recorded_by = request.user
            record.save()
            messages.success(request, 'Medical record saved successfully.')
            return redirect('student_detail', pk=student_pk)
        else:
            messages.error(request, 'Failed to save record. Please review form entries.')
    else:
        # Pre-select student identity and make the field read-only/hidden in standalone layouts
        form = MedicalRecordForm(initial={'student': student})
        
    return render(request, 'clinic/form.html', {'form': form, 'title': f'New Record — {student}'})


@login_required
def medical_record_delete(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Medical record deleted successfully!")
    return redirect('medical_record_list')


# ── APPOINTMENTS ───────────────────────────
@login_required
def appointment_list(request):
    appointments = Appointment.objects.all().order_by('date', 'time')
    return render(request, 'clinic/appointment_list.html', {'appointments': appointments})


@login_required
def appointment_add(request):
    form = AppointmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Appointment scheduled.')
        return redirect('appointment_list')
    return render(request, 'clinic/form.html', {'form': form, 'title': 'Schedule Appointment'})


@login_required
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    form = AppointmentForm(request.POST or None, instance=appointment)
    if request.method == 'POST' and form.is_valid():
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
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Medicine added to inventory.')
        return redirect('medicine_list')
    return render(request, 'clinic/medicine_form.html', {'form': form, 'title': 'Add Medicine', 'action': 'Add'})


@login_required
def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    form = MedicineForm(request.POST or None, instance=medicine)
    if request.method == 'POST' and form.is_valid():
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