from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, MedicalRecord, Appointment
from .forms import StudentForm, MedicalRecordForm, AppointmentForm

@login_required
def dashboard(request):
    context = {
        'total_students': Student.objects.count(),
        'upcoming_appointments': Appointment.objects.filter(
            status='Scheduled').order_by('date', 'time')[:5],
        'recent_records': MedicalRecord.objects.order_by('-date')[:5],
    }
    return render(request, 'clinic/dashboard.html', context)

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
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
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