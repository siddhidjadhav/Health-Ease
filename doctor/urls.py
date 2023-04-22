from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.doctor_dashboard, name="doctor_dashboard"),
    path('create_appointment', views.create_appointment, name="create_appointment"), 
]

