from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, MedicalRecord, Medicine, StockMovement, Appointment
from .forms import StudentForm, MedicalRecordForm, MedicineForm, StockMovementForm, AppointmentForm

@login_required
def dashboard(request):
    context = {
        'total_students': Student.objects.count(),
        'total_medicines': Medicine.objects.count(),
        'low_stock': Medicine.objects.filter(quantity__lte=10),
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
def medicine_list(request):
    medicines = Medicine.objects.all().order_by('name')
    return render(request, 'clinic/medicine_list.html', {'medicines': medicines})

@login_required
def medicine_add(request):
    form = MedicineForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Medicine added.')
        return redirect('medicine_list')
    return render(request, 'clinic/form.html', {'form': form, 'title': 'Add Medicine'})

@login_required
def stock_update(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    form = StockMovementForm(request.POST or None)
    if form.is_valid():
        movement = form.save(commit=False)
        movement.medicine = medicine
        movement.performed_by = request.user
        if movement.movement_type == 'IN':
            medicine.quantity += movement.quantity
        else:
            if medicine.quantity < movement.quantity:
                messages.error(request, 'Not enough stock.')
                return render(request, 'clinic/form.html', {'form': form, 'title': f'Update Stock — {medicine}'})
            medicine.quantity -= movement.quantity
        medicine.save()
        movement.save()
        messages.success(request, 'Stock updated.')
        return redirect('medicine_list')
    return render(request, 'clinic/form.html', {'form': form, 'title': f'Update Stock — {medicine}'})

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