from django.urls import path
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('', RedirectView.as_view(url='/login/'), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('student/edit/<int:pk>/', views.student_edit, name='student_edit'),
    path('records/add/<int:student_pk>/', views.record_add, name='record_add'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/add/', views.appointment_add, name='appointment_add'),
    path('appointment/edit/<int:pk>/', views.appointment_edit, name='appointment_edit'),
    path('appointment/delete/<int:pk>/', views.appointment_delete, name='appointment_delete'),
]