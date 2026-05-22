from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/login/'), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('student/edit/<int:pk>/', views.student_edit, name='student_edit'),

    # Records
    path('records/add/<int:student_pk>/', views.record_add, name='record_add'),

    # Appointments
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/add/', views.appointment_add, name='appointment_add'),
    path('appointment/edit/<int:pk>/', views.appointment_edit, name='appointment_edit'),
    path('appointment/delete/<int:pk>/', views.appointment_delete, name='appointment_delete'),

    # Medicines
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/add/', views.medicine_add, name='medicine_add'),
    path('medicines/edit/<int:pk>/', views.medicine_edit, name='medicine_edit'),
    path('medicines/delete/<int:pk>/', views.medicine_delete, name='medicine_delete'),
    path('medicines/restock/<int:pk>/', views.medicine_restock, name='medicine_restock'),
    path('medical-records/', views.medical_record_list, name='medical_record_list'),
    path('records/',views.medical_record_list, name='medical_records'),
    path('records/add/', views.medical_record_list, name='add_medical_record'),
]
    
