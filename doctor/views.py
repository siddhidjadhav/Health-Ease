from django.shortcuts import render, redirect
import re
from .utility import check_if_user_is_doctor
from django.contrib.auth import get_user_model
from .forms import AppointmentForm
from system.models import Appointment
from datetime import datetime
from django.utils import timezone
from django.contrib import messages


def doctor_dashboard(request):
    user_status = check_if_user_is_doctor(request.user)
    if not user_status["is_user_doctor"]:
        return redirect(user_status["user_identity"])
    # if not re.match(".@healthease.com$", user_email):
    #     message = "yes match"
    #     if re.search(".@gmail.com$", user_email):
    #         message = "yes"
    #         return redirect('patient_dashboard')


    todays_date = timezone.now().date()
    current_time = timezone.now()
    appointment_for_today = Appointment.objects.filter(date=todays_date, time__gt=current_time, doctor_id=request.user, patient_id__isnull=False)
    upcoming_appointments = Appointment.objects.filter(doctor_id=request.user).exclude(date=todays_date)
    booked_appointments = 0
    not_booked_appointments = 0
    total_appointments = len(appointment_for_today)
    for appointment in appointment_for_today:
        if appointment.patient_id:
            booked_appointments = booked_appointments+1
        else:
            not_booked_appointments = not_booked_appointments+1

    doctor = f"{request.user.first_name} {request.user.last_name}"
    return render(request, 'doctor_dashboard.html', { 'doctor':doctor, 'appointment_for_today':appointment_for_today, 'booked': booked_appointments, 'not_booked': not_booked_appointments, 'total_appointments': total_appointments, 'request': request})


def create_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')

        if appointment_id is not None:
            appointment = Appointment.objects.get(pk=appointment_id)
            appointment.delete()
            return redirect('create_appointment')

    if request.method == 'POST':
        # Retrieve the appointment date and time from the form data
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        
        # Convert the date and time strings to datetime objects
        datetime_str = f'{date_str} {time_str}'
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        
        # Create a new appointment object
        appointment = Appointment(date=datetime_obj.date(), time=datetime_obj.time(), doctor_id=request.user)
        appointment.save()
        return redirect('create_appointment')
    
    else:
        appointments = Appointment.objects.filter(doctor_id=request.user)
        return render(request, 'create_appointment.html', {'appointments': appointments})
    
