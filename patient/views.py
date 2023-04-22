from django.shortcuts import render, redirect
from datetime import date, timedelta
from .utility import check_if_user_is_patient
from django.contrib.auth import get_user_model
from system.models import Appointment
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def patient_dashboard(request):
    user_status = check_if_user_is_patient(request.user)
    if not user_status["is_user_patient"]:
        return redirect(user_status["user_identity"])
    if not request.user.is_authenticated:
        return redirect(f"{'/users/login'}?next={request.path}")
        
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        
        return redirect(f'book_appointment/{doctor_id}',)

    doctors = get_user_model().objects.filter(email__contains='@healthease.com').values()
    
    return render(request, 'patient_dashboard.html', {'doctors': doctors})

def doctor_details(request):
    doctor = {
        'name' : 'Manoj Kataria',
        'email' : 'manoj@gmail.com',
        'specialization' : 'MD, PHD',
        'address': 'Manas Hospital, Bharati Vidyapeth'
    }

    max_date = (date.today() + timedelta(days=6)).strftime("%Y-%m-%d")
    min_date = date.today().strftime("%Y-%m-%d")
    return render(request, 'doctor_info.html', {'doctor': doctor, 'min_date': min_date, 'max_date': max_date})

def patient_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        
        # Check if the appointment id is valid
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            appointment = None
        
        if appointment is not None:
            # If the appointment id is valid, assign the appointment to the current user
            appointment.patient_id = None
            appointment.save()
            return redirect('patient_appointment')
        
    appointments = Appointment.objects.filter(patient_id = request.user)
    return render(request, 'appointment.html', {'appointments': appointments})


def book_appointment(request, doctor_id):
    if request.method == 'POST':
        # Retrieve the selected date and appointment id from the form data
        selected_date_str = request.POST.get('selected_date')
        appointment_id = request.POST.get('appointment_id')
        
        # Check if the appointment id is valid
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            appointment = None
        
        if appointment is not None:
            # If the appointment id is valid, assign the appointment to the current user
            appointment.patient_id = request.user
            appointment.save()
            return redirect('patient_appointment')
        
    # If the request method is GET or the appointment id is not valid, display the calendar and appointments for the selected date
    if request.method == 'POST':
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    else:
        selected_date = datetime.now().date()
    
    doctor = user = get_object_or_404(User, id=doctor_id)
    appointments = Appointment.objects.filter(doctor_id=doctor, date=selected_date, patient_id=None)
    
    context = {
        'selected_date': selected_date,
        'appointments': appointments,
        'doctor_id': doctor
    }
    return render(request, 'book_appointment.html', context)