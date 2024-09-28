from django.db import models

# Create your models here.

class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField('Date of Birth')
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    medical_condition = models.CharField(max_length=100)
    medication_regimen = models.TextField()
    last_appointment = models.DateTimeField('Last Appointment')
    next_appointment = models.DateTimeField('Next Appointment')
    doctor_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Conversation(models.Model):
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    message = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField()