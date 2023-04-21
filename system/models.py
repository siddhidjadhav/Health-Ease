from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Appointment(models.Model):
    patient_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient", null=True, blank=True)
    doctor_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor")
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Appointment is on {self.date}"
