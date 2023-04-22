from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.patient_dashboard, name="patient_dashboard"),
    path('doctor_details', views.doctor_details, name="doctor_details"),
    path('patient_appointment', views.patient_appointment, name="patient_appointment"),
    path('book_appointment/<doctor_id>', views.book_appointment, name="book_appointment"),
]



