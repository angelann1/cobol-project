from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, MedicalRecord, Appointment
from .forms import StudentForm, MedicalRecordForm, AppointmentForm


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