# Generated by Django 5.1.1 on 2024-09-23 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_bot', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('dob', models.DateField(verbose_name='Date of Birth')),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('medical_condition', models.CharField(max_length=100)),
                ('medication_regimen', models.TextField()),
                ('last_appointment', models.DateTimeField(verbose_name='Last Appointment')),
                ('next_appointment', models.DateTimeField(verbose_name='Next Appointment')),
                ('doctor_name', models.CharField(max_length=50)),
            ],
        ),
    ]
